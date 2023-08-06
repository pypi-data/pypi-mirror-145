import importlib.resources as pkg_resources
import os
from pathlib import Path
import pwd
import shutil
import subprocess

from jinja2 import Environment, PackageLoader
import pandas as pd

from .. import pipelines


class CeligoSingleImageCore:

    """
    This Class provides utility functions for the Celigo
    pipeline to prepare single images for:

    1) Ilastik Processing

    2) Cell Profiler Processing

    Given its large processing needs it is set up to run on slurm

    """

    def __init__(self, raw_image_path):

        # Specific name of experiment
        self.tempdirname = Path(raw_image_path).with_suffix("").name

        # Working Directory
        if not os.path.exists(
            f"/home/{pwd.getpwuid(os.getuid())[0]}/{self.tempdirname}"
        ):
            os.mkdir(f"/home/{pwd.getpwuid(os.getuid())[0]}/{self.tempdirname}")
        self.working_dir = Path(
            f"/home/{pwd.getpwuid(os.getuid())[0]}/{self.tempdirname}"
        )

        # Image Paths
        self.raw_image_path = Path(raw_image_path)

        shutil.copyfile(
            self.raw_image_path, f"{self.working_dir}/{self.raw_image_path.name}"
        )
        self.image_path = Path(f"{self.working_dir}/{self.raw_image_path.name}")

        # Future resource paths
        self.filelist_path = Path()
        self.resize_filelist_path = Path()
        self.cell_profiler_output_path = Path()

        self.downsample_job_ID = int()
        self.ilastik_job_ID = int()
        self.cellprofiler_job_ID = int()

        # Pipeline paths for templates
        with pkg_resources.path(pipelines, "rescale_pipeline.cppipe") as p:
            self.rescale_pipeline_path = p
        with pkg_resources.path(pipelines, "96_well_colony_pipeline.cppipe") as p:
            self.cellprofiler_pipeline_path = p
        with pkg_resources.path(pipelines, "colony_morphology.model") as p:
            self.classification_model_path = p

        '''
        # replacing folder refrence location in cell profiler pipeline file with new location of classification model
        fin = open(self.cellprofiler_pipeline_path, "rt")
        data = fin.read()
        data = data.replace(
            "\\\\\\\\allen\\\\aics\\\\microscopy\\\\CellProfiler_4.1.3_Testing\\\\4.2.1_PipelineUpdate",
            str(self.classification_model_path.parent),
        )

        fin.close()
        fin = open(self.cellprofiler_pipeline_path, "wt")
        fin.write(data)
        fin.close()
        
        # Temporary for testing
        shutil.copyfile(
            self.cellprofiler_pipeline_path, f"{self.working_dir}/{self.cellprofiler_pipeline_path.name}"
        )
        '''

    def downsample(self):
        # Generates a filelist
        with open(self.working_dir / "resize_filelist.txt", "w+") as rfl:
            rfl.write(str(self.image_path) + "\n")

        self.resize_filelist_path = self.working_dir / "resize_filelist.txt"

        # Defines variables for bash script
        script_config = {
            "filelist_path": str(self.resize_filelist_path),
            "output_path": str(self.working_dir),
            "pipeline_path": str(self.rescale_pipeline_path),
        }

        # Generates script_body from existing templates.
        jinja_env = Environment(
            loader=PackageLoader(
                package_name="celigo_pipeline_core", package_path="templates"
            )
        )
        script_body = jinja_env.get_template("resize_cellprofiler_template.j2").render(
            script_config
        )

        # Creates bash script locally.
        with open(self.working_dir / "resize.sh", "w+") as rsh:
            rsh.write(script_body)

        # Runs resize on slurm
        output = subprocess.run(
            ["sbatch", f"{str(self.working_dir)}/resize.sh"],
            check=True,
            capture_output=True,
        )

        # Sets path to resized image to image path for future use
        self.image_path = (
            self.image_path.parent
            / f"{self.image_path.with_suffix('').name}_rescale.tiff"
        )

        job_ID = int(output.stdout.decode("utf-8").split(" ")[-1][:-1])
        return job_ID, self.image_path

    def run_ilastik(self):

        # Parameters to input to bash script template
        script_config = {
            "image_path": f"'{str( self.image_path)}'",
            "output_path": f"'{str(self.image_path.with_suffix(''))}_probabilities.tiff'",
        }

        # Generates script_body from existing templates.
        jinja_env = Environment(
            loader=PackageLoader(
                package_name="celigo_pipeline_core", package_path="templates"
            )
        )

        script_body = jinja_env.get_template("ilastik_template.j2").render(
            script_config
        )

        # Creates bash script locally.
        with open(self.working_dir / "ilastik.sh", "w+") as rsh:
            rsh.write(script_body)

        # Runs ilastik on slurm
        output = subprocess.run(
            ["sbatch", f"{str(self.working_dir)}/ilastik.sh"],
            check=True,
            capture_output=True,
        )

        # Creates filelist.txt
        with open(self.working_dir / "filelist.txt", "w+") as rfl:
            rfl.write(str(self.image_path) + "\n")
            rfl.write(str(self.image_path.with_suffix("")) + "_probabilities.tiff")

        self.filelist_path = self.working_dir / "filelist.txt"
        job_ID = int(output.stdout.decode("utf-8").split(" ")[-1][:-1])
        return job_ID, Path(f"{self.image_path.with_suffix('')}_probabilities.tiff")

    def run_cellprofiler(self):

        # Parameters to input to bash script template.
        script_config = {
            "filelist_path": str(self.filelist_path),
            "output_dir": str(self.working_dir / "cell_profiler_outputs"),
            "pipeline_path": str(self.cellprofiler_pipeline_path),
        }

        # Generates script_body from existing templates.
        jinja_env = Environment(
            loader=PackageLoader(
                package_name="celigo_pipeline_core", package_path="templates"
            )
        )
        script_body = jinja_env.get_template("cellprofiler_template.j2").render(
            script_config
        )

        # Creates bash script locally.
        with open(self.working_dir / "cellprofiler.sh", "w+") as rsh:
            rsh.write(script_body)

        # Runs cellprofiler on slurm
        output = subprocess.run(
            ["sbatch", f"{str(self.working_dir)}/cellprofiler.sh"],
            check=True,
            capture_output=True,
        )

        # Returns path to directory of cellprofiler outputs
        self.cell_profiler_output_path = self.working_dir / "cell_profiler_outputs"
        job_ID = int(output.stdout.decode("utf-8").split(" ")[-1][:-1])
        return (
            job_ID,
            Path(script_config["output_dir"]),
        )  # TODO change this to the last output

    def upload_metrics(self):
        # combine output metrics and send to database

        BallCraterDATA = pd.read_csv(
            self.cell_profiler_output_path / "BallCraterDATA.csv"
        )
        ColonyDATA = pd.read_csv(self.cell_profiler_output_path / "ColonyDATA.csv")
        ImageDATA = pd.read_csv(self.cell_profiler_output_path / "ImageDATA.csv")
        ExperimentDATA = pd.read_csv(
            self.cell_profiler_output_path / "ExperimentDATA.csv"
        )

        # combine metrics

        # Send to DB

    def cleanup(self):
        shutil.rmtree(self.working_dir)

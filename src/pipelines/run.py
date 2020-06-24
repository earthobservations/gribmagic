""" command line entry points for nwp data download """
import fire

from src.pipelines.pipelines import run_model_download


if __name__ == '__main__':
  fire.Fire({
      'run_model_download': run_model_download
})

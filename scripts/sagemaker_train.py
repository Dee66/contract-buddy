import argparse
import os
import sys
import logging
import yaml
import sagemaker
from sagemaker.estimator import Estimator
from pathlib import Path


def load_config(config_path: str) -> dict:
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Launch a SageMaker training job.")
    parser.add_argument(
        "--config", type=str, required=True, help="Path to config YAML file."
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    config = load_config(args.config)

    # Extract SageMaker and training parameters from config
    sagemaker_cfg = config.get("sagemaker", {})
    role_arn = sagemaker_cfg.get("role_arn") or os.environ.get("SAGEMAKER_ROLE_ARN")
    if not role_arn:
        logging.critical(
            "SageMaker execution role ARN must be set in config or SAGEMAKER_ROLE_ARN env var."
        )
        sys.exit(1)

    image_uri = sagemaker_cfg.get("image_uri")
    if not image_uri:
        logging.critical(
            "SageMaker training image URI must be set in config['sagemaker']['image_uri']."
        )
        sys.exit(1)

    instance_type = sagemaker_cfg.get("instance_type", "ml.m5.large")
    instance_count = int(sagemaker_cfg.get("instance_count", 1))
    output_path = (
        sagemaker_cfg.get("output_path")
        or f"s3://{sagemaker_cfg.get('bucket')}/output/"
    )
    hyperparameters = sagemaker_cfg.get("hyperparameters", {})

    # Optional: input data channels
    input_data = sagemaker_cfg.get("input_data", {})
    channels = {}
    for channel_name, s3_uri in input_data.items():
        channels[channel_name] = sagemaker.inputs.TrainingInput(s3_uri)

    session = sagemaker.Session()
    estimator = Estimator(
        image_uri=image_uri,
        role=role_arn,
        instance_count=instance_count,
        instance_type=instance_type,
        output_path=output_path,
        hyperparameters=hyperparameters,
        sagemaker_session=session,
        enable_sagemaker_metrics=True,
    )

    logging.info(f"Launching SageMaker training job with image: {image_uri}")
    try:
        estimator.fit(channels if channels else None, wait=True)
        logging.info("SageMaker training job completed successfully.")
    except Exception as e:
        logging.critical(f"SageMaker training job failed: {e}", exc_info=True)
        sys.exit(2)


if __name__ == "__main__":
    main()

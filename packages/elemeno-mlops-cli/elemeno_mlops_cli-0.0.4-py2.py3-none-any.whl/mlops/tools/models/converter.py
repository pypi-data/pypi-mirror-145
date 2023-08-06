import os
from typing import Optional, Tuple
import click
from elemeno_ai_sdk.models.conversion.converter import ModelConverter

def convert(model_path, input_dims: Optional[Tuple[int]] = None):
    if not os.path.exists(model_path):
        click.echo("FAILED. Model file does not exist")
        return -1
    converter = ModelConverter(model_path, input_dims=input_dims)
    converter.apply_conversion()
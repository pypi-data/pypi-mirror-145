import click
from .models.converter import convert as model_converter

@click.group(name="tools")
def tools():
  pass

@tools.command(name="model.convert", help="Convert a model to onnx")
@click.option('--model-path', type=str, required=True, help="The path to the model to be converted")
@click.option('--input-dims', type=(int, int), required=False, help="The input dimensions of the model")
def convert(model_path, input_dims):
    """Convert a model to onnx
    MODEL_PATH - the path to the model to be converted
    """
    model_converter(model_path, input_dims)
    click.echo("Model converted to onnx")

if __name__ == '__main__':
  tools.add_command(convert)
  tools()
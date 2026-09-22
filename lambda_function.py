import boto3

import os

import io

from PIL import Image


s3 = boto3.client('s3')

OUTPUT_BUCKET = 'my-images-resized'

MAX_WIDTH  = 800

MAX_HEIGHT = 800


def lambda_handler(event, context):

    record       = event['Records'][0]

    input_bucket = record['s3']['bucket']['name']

    key          = record['s3']['object']['key']

    print(f'Processing: s3://{input_bucket}/{key}')


    # Download image into memory

    response   = s3.get_object(Bucket=input_bucket, Key=key)

    image_data = response['Body'].read()


    # Open and resize

    image         = Image.open(io.BytesIO(image_data))

    original_size = image.size

    image.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.LANCZOS)


    # Determine format and content type

    fmt = image.format or 'JPEG'

    content_type_map = {

        'JPEG': 'image/jpeg', 'PNG': 'image/png',

        'WEBP': 'image/webp', 'GIF': 'image/gif',

    }

    content_type = content_type_map.get(fmt, 'image/jpeg')


    # Save to memory buffer

    buffer = io.BytesIO()

    image.save(buffer, format=fmt)

    buffer.seek(0)


    # Upload to output bucket

    output_key = f'resized_{os.path.basename(key)}'

    s3.put_object(Bucket=OUTPUT_BUCKET, Key=output_key,

                  Body=buffer, ContentType=content_type)


    new_size = image.size

    print(f'Done: {original_size} -> {new_size}, saved to {output_key}')

    return {'statusCode': 200,

            'body': f'Resized {key}: {original_size} -> {new_size}'}

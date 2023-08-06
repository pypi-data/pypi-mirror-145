"""
The HEA Server Buckets Microservice provides ...
"""
import http.client
import json
from typing import Optional, Dict, Union

from heaobject.root import Permission
from heaserver.service import response, appproperty
from heaserver.service.appproperty import HEA_DB
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import awsservicelib, mongo, mongoservicelib
from heaserver.service.wstl import builder_factory, action
from heaobject.bucket import Bucket
from heaserver.service.oidcclaimhdrs import SUB

MONGODB_BUCKET_COLLECTION = 'buckets'


@routes.get('/volumes/{volume_id}/buckets/{id}')
async def get_bucket(request: web.Request) -> web.Response:
    """
    Gets the bucket with the specified id.
    :param request: the HTTP request.
    :return: the requested bucket or Not Found.
    ---
    summary: A specific bucket.
    tags:
        - buckets
    parameters:
        - name: id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: hci-foundation
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """

    return await awsservicelib.get_bucket(request=request)


@routes.get('/volumes/{volume_id}/buckets/byname/{bucket_name}')
async def get_bucket_by_name(request: web.Request) -> web.Response:
    """
    Gets the bucket with the specified name.
    :param request: the HTTP request.
    :return: the requested bucket or Not Found.
    ---
    summary: A specific bucket.
    tags:
        - buckets
    parameters:
        - name: bucket_name
          in: path
          required: true
          description: The name of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: Name of the bucket
              value: hci-foundation
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_bucket(request=request)


@routes.get('/volumes/{volume_id}/buckets')
async def get_all_buckets(request: web.Request) -> web.Response:
    """
    Gets all buckets.
    :param request: the HTTP request.
    :return: all buckets.
    ---
    summary: get all buckets for a hea-volume associate with account.
    tags:
        - buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_all_buckets(request)


@routes.get('/ping')
async def ping(request: web.Request) -> web.Response:
    """
    For testing whether the service is up.

    :param request: the HTTP request.
    :return: Always returns status code 200.
    """
    return response.status_ok(None)


@routes.post('/volumes/{volume_id}/buckets')
async def post_bucket(request: web.Request) -> web.Response:
    """
    Posts the provided bucket.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    ---
    summary: Bucket Creation
    tags:
        - buckets
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    requestBody:
      description: Attributes of new Bucket.
      required: true
      content:
        application/vnd.collection+json:
          schema:
            type: object
          examples:
            example:
              summary: Bucket example
              value: {
                "template": {
                  "data": [{
                    "name": "created",
                    "value": null
                  },
                  {
                    "name": "derived_by",
                    "value": null
                  },
                  {
                    "name": "derived_from",
                    "value": []
                  },
                  {
                    "name": "description",
                    "value": null
                  },
                  {
                    "name": "display_name",
                    "value": "hci-test-bucket"
                  },
                  {
                    "name": "invited",
                    "value": []
                  },
                  {
                    "name": "modified",
                    "value": null
                  },
                  {
                    "name": "name",
                    "value": "hci-test-bucket"
                  },
                  {
                    "name": "owner",
                    "value": "system|none"
                  },
                  {
                    "name": "shared_with",
                    "value": []
                  },
                  {
                    "name": "source",
                    "value": null
                  },
                  {
                    "name": "version",
                    "value": null
                  },
                  {
                    "name": "encrypted",
                    "value": true
                  },
                  {
                    "name": "versioned",
                    "value": false
                  },
                  {
                    "name": "locked",
                    "value": false
                  },
                  {
                    "name": "tags",
                    "value": []
                  },
                  {
                    "name": "region",
                    "value": us-west-2
                  },
                  {
                    "name": "permission_policy",
                    "value": null
                  }]
                }
              }
        application/json:
          schema:
            type: object
          examples:
            example:
              summary: Bucket example
              value: {
                "created": null,
                "derived_by": null,
                "derived_from": [],
                "description": "This is a description",
                "display_name": "hci-test-bucket",
                "invited": [],
                "modified": null,
                "name": "hci-test-bucket",
                "owner": "system|none",
                "shared_with": [],
                "source": null,
                "type": "heaobject.bucket.AWSBucket",
                "version": null,
                encrypted: true,
                versioned: false,
                locked: false,
                tags: [],
                region: "us-west-2",
                permission_policy: null
              }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.post_bucket(request=request)


@routes.put('/volumes/{volume_id}/buckets/{id}')
async def put_bucket(request: web.Request) -> web.Response:
    """
    Updates the bucket with the specified id.
    :param request: the HTTP request.
    :return: a Response object with a status of No Content or Not Found.
    """
    return await mongoservicelib.put(request, MONGODB_BUCKET_COLLECTION, Bucket)


@routes.delete('/volumes/{volume_id}/buckets/{id}')
async def delete_bucket(request: web.Request) -> web.Response:
    """
    Deletes the bucket with the specified id.
    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: A specific bucket.
    tags:
        - buckets
    parameters:
        - name: id
          in: path
          required: true
          description: The id of the bucket to delete.
          schema:
            type: string
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.delete_bucket(request)


# Object/File rest points below
@routes.get('/volumes/{volume_id}/buckets/byname/{bucket_name}/objects')
async def get_all_bucket_objects(request: web.Request) -> web.Response:
    """
    Gets all bucket with the specified id.
    :param request: the HTTP request.
    :return: a list of requested bucket objects or Not Found.
    ---
    summary: Gets all objects within bucket paginated.
    tags:
        - buckets
    parameters:
        - name: bucket_name
          in: path
          required: true
          description: The name of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket name
              value: hci-foundation
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: start_after_key
          in: query
          schema:
            type: string
          description: s3 key for object to start after in pagination/
        - name: max_keys
          in: query
          schema:
            type: integer
          description: maximum keys to return at a time to paginate through
        - in: query
          name: page_size
          schema:
            type: integer
          description: each page size
        - in: query
          name: starting_token
          schema:
            type: string
          description: The continuation token to advance to specific page
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_all(request=request)


@routes.get('/volumes/{volume_id}/buckets/byname/{bucket_name}/folders/objects')
async def get_bucket_folder_objects(request: web.Request) -> web.Response:
    """
    Gets all object in specified folder of bucket.
    :param request: the HTTP request.
    :return: the requested bucket objects or Not Found.
    ---
    summary: Retrieve s3 objects given a folder name .
    tags:
        - buckets
    parameters:
        - name: bucket_name
          in: path
          required: true
          description: The name of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket name
              value: hci-foundation
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: start_after_key
          in: query
          schema:
            type: string
          description: s3 key for object to start after in pagination/
        - name: max_keys
          in: query
          schema:
            type: integer
          description: maximum keys to return at a time to paginate through
        - in: query
          name: page_size
          schema:
            type: integer
          description: each page size
        - in: query
          name: starting_token
          schema:
            type: string
          description: The continuation token to advance to specific page
        - name: folder_name
          in: query
          description: This is prefix or folder for s3 objects.
          schema:
            type: string
          examples:
            example:
              summary: A folder name
              value: 'scripts'
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_all(request=request, by_dir_level=True)


@routes.get('/volumes/{volume_id}/buckets/byname/{bucket_name}/objects/{path}/content')
async def get_bucket_object_content(request: web.Request) -> web.Response:
    """
    Gets a single object's as File Stream
    :param request: the HTTP request.
    :return: the requested bucket objects or Not Found.
    """
    return await awsservicelib.get_object_content(request=request)


@routes.post('/volumes/{volume_id}/buckets/byname/{bucket_name}/objects')
async def post_bucket_object(request: web.Request) -> web.Response:
    """
    Creates a single object
    :param request: the HTTP request.
    :return: HTTP Created or Not Found.
    """
    return await awsservicelib.post_object(request=request)


@routes.delete('/volumes/{volume_id}/buckets/byname/{bucket_name}/objects/{path}')
async def delete_bucket_object(request: web.Request) -> web.Response:
    """
    Deletes a single object
    :param request: the HTTP request.
    :return: the requested bucket objects or Not Found.
    """
    return await awsservicelib.delete_object(request=request)


# @routes.get('/volumes/{volume_id}/byname/{name}/object/{path_name}')
# async def download_bucket_object(request: web.Request) -> web.Response:
#     """
#     Gets all object in specified folder of bucket.
#     :param request: the HTTP request.
#     :return: the requested bucket objects or Not Found.
#     """
#     return await awsservicelib.download_object(request=request, volume_id=request.match_info['volume_id'],
#                                                   bucket_name=request.match_info['name'],
#                                                   path_name=request.match_info['folder_name'])


def main() -> None:
    config = init_cmd_line(description='a service for managing buckets and their data within the cloud',
                           default_port=8080)
    start(db=mongo.Mongo, wstl_builder_factory=builder_factory(__package__), config=config)

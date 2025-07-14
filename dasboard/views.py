
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from pathlib import Path
from django.core.files.storage import default_storage
from django.conf import settings
from wsgiref.util import FileWrapper
import mimetypes


class FileDownloadAPIView(APIView):
    """
    API endpoint that allows users to download files.
    
    Required parameters:
    - file_path: Relative path to the file in the storage system
    (e.g., "documents/reports/report_2023.pdf")
    
    Optional parameters:
    - as_attachment: Boolean (default True) - download as attachment vs inline
    """
    
    def get(self, request):
        # Get file path from query parameters
        file_path = request.query_params.get('file_path')
        
        # Validate required parameter
        if not file_path:
            return Response(
                {"error": "file_path parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Security check - prevent directory traversal
        try:
            full_path = default_storage.path(file_path)
            print(f"Resolved full path: {full_path}")  # Debugging line
            
            # Validate the resolved path is within the media root
            media_root = Path(settings.MEDIA_ROOT).resolve()
            if not Path(full_path).resolve().is_relative_to(media_root):
                return Response(
                    {"error": "Access to requested file location is denied"},
                    status=status.HTTP_403_FORBIDDEN
                )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Error resolving file path: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Check if file exists
        if not default_storage.exists(file_path):
            return Response(
                {"error": "File not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Open the file for reading
        try:
            file = default_storage.open(file_path, 'rb')
            
            # Determine content type
            content_type, _ = mimetypes.guess_type(file_path)
            if not content_type:
                content_type = 'application/octet-stream'
                
            # Determine if we should force download (attachment) or display inline
            as_attachment = request.query_params.get('as_attachment', 'true').lower() == 'true'
            
            # Extract filename
            filename = os.path.basename(file_path)
            
            # Create and return the response
            response = FileResponse(
                FileWrapper(file),
                content_type=content_type,
                as_attachment=as_attachment,
                filename=filename
            )
            
            # Set appropriate headers for downloads
            response['Content-Length'] = default_storage.size(file_path)
            response['Content-Disposition'] = (
                f'attachment; filename="{filename}"' if as_attachment 
                else f'inline; filename="{filename}"'
            )
            
            return response
            
        except Exception as e:
            return Response(
                {"error": f"Error accessing file: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )







# class FileDownloadView(APIView):
#     """
#     API View for downloading files from external URLs.
#     Example POST request:
#     {
#         "file_url": "https://example.com/path/to/file.pdf"
#     }
#     """
    
#     def post(self, request):
#         file_url = request.data.get('file_url')
        
#         if not file_url:
#             return Response(
#                 {"error": "File URL is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         try:
#             # Stream the file from the given URL
#             response = requests.get(file_url, stream=True)
            
#             if response.status_code != 200:
#                 return Response(
#                     {"error": f"Failed to fetch file from URL. Status code: {response.status_code}"},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
            
#             # Determine filename from URL or content-disposition
#             filename = os.path.basename(file_url)
            
#             if 'content-disposition' in response.headers:
#                 # Extract filename from content-disposition if available
#                 content_disposition = response.headers['content-disposition']
#                 filename_start = content_disposition.find('filename=')
#                 if filename_start != -1:
#                     filename = content_disposition[filename_start + len('filename='):].strip('"\'')
            
#             # Determine content type
#             content_type = response.headers.get('content-type')
#             if not content_type:
#                 content_type, _ = mimetypes.guess_type(filename)
                
#             # Create a file-like object from the response content
#             file_like = BytesIO(response.content)
            
#             # Create a streaming response
#             response = FileResponse(
#                 file_like,
#                 content_type=content_type,
#                 as_attachment=True,
#                 filename=filename
#             )
            
#             return response
            
#         except requests.exceptions.RequestException as e:
#             return Response(
#                 {"error": f"Error downloading file: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
#         except Exception as e:
#             return Response(
#                 {"error": f"Unexpected error: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )





class GrabUrlItemApiViews(APIView):

    def get(self,request,item):
        query = Luxury_car.objects.all()
        serialize_class = CarSerializer

        serializedata = serialize_class(query, many = True)

        return Response(serializedata.data)
    





class GrabParameterItemApiView(APIView):

    def get(self, request, pk):
        query = get_object_or_404(Luxury_car, pk)
        serialize_class = CarSerializer
        serializedata = serialize_class(query)
        if serializedata.is_valid():
            return Response(serializedata.data)
        
        return Response({"not found":"could not successful get the item"})
    
    

class Registerproduct(APIView):

    def post(self, request):
        serializedata = CarSerializer(data=request.data)   
        if serializedata.is_valid():
            return Response(serializedata.data,status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)



class ShowAllItemApiView(APIView):
    
    def get(self, request):
        items = Luxury_car.objects.get_queryset()
        return Response("hello world")


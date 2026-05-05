# ===========================
# 🔹 IMPORTS
# ===========================
from django.shortcuts import get_object_or_404, render,redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

#Day - 5
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobApplicationFilter
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

#Day 6 ViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

#Day 7
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#Day 8
from .forms import JobApplicationForm
from .serializers import JobApplicationSerializer
from .models import JobApplication

#Day 9
from django.core.paginator import Paginator


@login_required
def dashboard(request):
    jobs_list = JobApplication.objects.filter(
        owner = request.user
    ).order_by('-date_applied')
    
    # Search filter — URL se ?search=google
    search_query = request.GET.get('search','')
    
    if search_query:
        jobs_list = jobs_list.filter(
            company__icontains=search_query
        ) | jobs_list.filter(
            role__icontains=search_query
        ) 
        
    # Status filter — URL se ?status=applied
    status_filter = request.GET.get('status', '')
    if status_filter:
        jobs_list = jobs_list.filter(status=status_filter)  
    paginator = Paginator(jobs_list,5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    all_jobs = JobApplication.objects.filter(owner=request.user)
    
    stats = {
        'total':     jobs_list.count(),
        'applied':   jobs_list.filter(status='applied').count(),
        'interview': jobs_list.filter(status='interview').count(),
        'offer':     jobs_list.filter(status='offer').count(),
        'rejected':  jobs_list.filter(status='rejected').count(),
    }
    
    return render(request, 'dashboard.html',{
        'page_obj': page_obj,
        'jobs_list':jobs_list,
        'stats':stats,
        'search_query':search_query,
        'status_filter' : status_filter
    })
    
@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job = form.save(commit = False)
            job.owner = request.user
            job.save()
            messages.success(request, 'Job application has been added')
            return redirect('dashboard')
    else:
        form = JobApplicationForm()
            
        return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Add New Job'})
@login_required
def job_edit(request, pk):
    job = get_object_or_404(JobApplication, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job update ho gayi!')
            return redirect('dashboard')
    else:
        form = JobApplicationForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Job Edit Karo'})


@login_required
def job_delete(request, pk):
    job = get_object_or_404(JobApplication, pk=pk, owner=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job delete ho gayi!')
        return redirect('dashboard')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.post)
        if form.is_valid():
            user = form.save()
            login(request, login )
            messages.success(request, f"Account has been created, Welcome{user.username}")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'regitration/register.html', {'form':form})   


#Day 6 ViewSet (Dhoni)
class JobApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filter_class = JobApplicationFilter
    
    search_fileds = ['company', 'status']
    order_fileds = ['date_applied', 'salary']
    ordering = ['-date_applied']
    
    def get_queryset(self):
        return JobApplication.objects.filter(owner = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self.get_queryset()
        stats = {
            'total' : queryset.count(),
            'applied' : queryset.filter(status = 'applied').count(),
            'interview' : queryset.filter(status = 'interview').count(),
            'rejected' : queryset.filter(status = 'rejected').count(),
            'offer' : queryset.filter(status = 'offer').count(),
        }   
        return Response(stats)


# =============================
# 🔹FUNCTION BASED VIEWS (FBV)
# =============================

# @api_view(['GET', 'POST'])
# def job_list(request):

#     if request.method == 'GET':
#         jobs = JobApplication.objects.all()
#         serializer = JobApplicationSerializer(jobs, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = JobApplicationSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def job_details(request, id):
#     jobs = get_object_or_404(JobApplication, id=id)
#     serializer = JobApplicationSerializer(jobs)
#     return Response(serializer.data)


# ===========================
# 🔹 CLASS BASED VIEWS (CBV)
# ===========================

# class job_list(APIView):

#     def get(self, request):
#         jobs = JobApplication.objects.all()
#         serializer = JobApplicationSerializer(jobs, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = JobApplicationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


# class job_details(APIView):

#     def get_objects(self, pk):
#         try:
#             return JobApplication.objects.get(pk=pk)
#         except JobApplication.DoesNotExist:
#             return None

#     def get(self, request, pk):
#         job = self.get_objects(pk)
#         if job is None:
#             return Response({'error': 'job not found'}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = JobApplicationSerializer(job)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def put(self, request, pk):
#         job = self.get_objects(pk)
#         if job is None:
#             return Response({'error': 'job not found'}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = JobApplicationSerializer(job, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         job = self.get_objects(pk)
#         if job is None:
#             return Response({'error': 'job not found'}, status=status.HTTP_400_BAD_REQUEST)

#         job.delete()
#         return Response(  )


# ===========================
# 🔹 MIXINS VERSION
# ===========================

# class job_list(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     generics.GenericAPIView
# ):
#     queryset = JobApplication.objects.all()
#     serialize_class = JobApplicationSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class job_detail(
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     generics.GenericAPIView
# ):
#     queryset = JobApplication.objects.all()
#     serializer_class = JobApplicationSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# ===========================
# 🔹 GENERIC VIEWS (ACTIVE)
# ===========================

# class job_list(generics.ListCreateAPIView):

#     serializer_class = JobApplicationSerializer
#     permission_classes = [IsAuthenticated] #Only Logged in Users

#     #Day 5 Filtering Data
#     filter_backends=[
#         DjangoFilterBackend,
#         filters.OrderingFilter,
#         filters.SearchFilter
#     ]
#     # DjangoFilterBackend ke liye — kon se fields filter honge    
#     filterset_fields = ['status', 'company']

#     # SearchFilter ke liye — kon se fields mein search hoga
#     searchset_fields = ['notes', 'company', 'role']

#     # OrderingFilter ke liye — kon se fields se sort kar sakte hain
#     ordering_fiedls = ['salary', 'date_applied']

#     # Default ordering — agar user kuch specify na kare
#     ordering = ['-date_applied']   # Latest first by default

#     #Throtling
#     throttle_classes = [UserRateThrottle]# Override global setting
#     """
#     If request Hit limit    :
#     HTTP 429 Too Many Requests
#         {
#     "detail": "Request was throttled. Expected available in 86400 seconds."
#         }
#     """

#     #Updated Part
#     def get_queryset(self):
#         queryset = JobApplication.objects.filter(owner = self.request.user)
#         status = self.request.query_params.get('status')
#         if status :
#             queryset = queryset.filter(status=status.lower())
#         return queryset

#     def perform_create(self, serializer):
#         serializer.save(owner = self.request.user)

# class job_detail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = JobApplication.objects.all()
#     serializer_class = JobApplicationSerializer
#     permission_classes = [IsAuthenticated]

#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

#     search_fields = ['company', 'role', 'notes']
#     ordering_fields = ['salary', 'date_applied']
#     ordering = ['-date_applied']
#     filterset_class = JobApplicationFilter

#     def get_queryset(self):
#         return JobApplication.objects.filter(
#             owner = self.request.user
#         )
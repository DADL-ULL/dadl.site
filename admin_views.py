# admin_views.py - Enhanced with file upload support
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import FileUploadField, ImageUploadField
from flask_login import current_user
from flask import redirect, url_for, request
from wtforms import validators
import os
import PIL.Image
from wtforms import SelectField

from models import Student


if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

# Base Admin Views
class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login', next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login', next=request.url))
    
    @expose('/')
    def index(self):
        from models import Student, Project, Publication
        
        total_students = Student.query.count()
        current_students = Student.query.filter_by(is_current=True).count()
        total_projects = Project.query.count()
        active_projects = Project.query.filter_by(status='Ongoing').count()
        total_publications = Publication.query.count()
        
        return self.render('admin/index.html', 
                          current_user=current_user,
                          logout_url=url_for('admin_logout'),
                          total_students=total_students,
                          current_students=current_students,
                          total_projects=total_projects,
                          active_projects=active_projects,
                          total_publications=total_publications)

# Custom Model Views with File Upload Support
from flask_admin.form.upload import FileUploadField
import os

class ProfessorModelView(AuthenticatedModelView):
    column_list = ['name', 'title', 'email', 'office', 'photo']
    column_searchable_list = ['name', 'email', 'title']
    
    # Use FileUploadField instead of ImageUploadField
    form_overrides = {
        'photo': FileUploadField
    }
    
    form_args = {
        'photo': {
            'label': 'Profile Photo',
            'base_path': 'static/uploads/professor',
            'allowed_extensions': ['jpg', 'jpeg', 'png', 'gif']
        }
    }
    
    # Display image in admin list
    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''
        return f'<img src="/static/uploads/professor/{model.photo}" width="50" style="object-fit: cover;">'
    
    column_formatters = {
        'photo': _list_thumbnail
    }

    def on_model_change(self, form, model, is_created):
        # Clean up old photo when replacing
        if not is_created and hasattr(form, 'photo') and form.photo.data:
            # Get the old photo from database
            from app import db, Professor
            old_professor = db.session.query(Professor).filter_by(id=model.id).first()
            if old_professor and old_professor.photo and old_professor.photo != model.photo:
                old_path = os.path.join('static/uploads/professor', old_professor.photo)
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except:
                        pass  # Ignore if file doesn't exist
        
        return super().on_model_change(form, model, is_created)


class StudentModelView(AuthenticatedModelView):
    column_list = ['name', 'degree_type', 'school', 'is_current', 'start_date', 'photo']
    column_filters = ['degree_type', 'is_current', 'school']
    column_searchable_list = ['name', 'research_focus']
    form_excluded_columns = ['created_at', 'projects']
    
    form_overrides = {
        'photo': ImageUploadField,
        'degree_type': SelectField  
    }
    
    form_args = {
        'photo': {
            'label': 'Student Photo',
            'base_path': 'static/uploads/students',
            'url_relative_path': 'uploads/students/',
            'allowed_extensions': ['jpg', 'jpeg', 'png', 'gif'],
            'max_size': (600, 600, True),
            'thumbnail_size': (100, 100, True),
            'validators': [validators.Optional()]
        },
        'degree_type': {
            'choices': [('PhD', 'PhD'), ('Masters', 'Masters')],
            'coerce': str
        }
    }
    
    def _list_thumbnail(view, context, model, name):
        if not model.photo:
            return ''
        return f'<img src="/{view.form_args["photo"]["url_relative_path"]}{model.photo}" width="50">'
    
    column_formatters = {
        'photo': _list_thumbnail
    }

from flask_admin.contrib.sqla.fields import QuerySelectMultipleField

class ProjectModelView(AuthenticatedModelView):
    column_list = ['title', 'topic', 'status', 'start_date', 'members', 'image1', 'image2', 'image3', 'image4']
    column_filters = ['status', 'topic']
    column_searchable_list = ['title', 'overview']
    form_excluded_columns = ['created_at']
    
    form_overrides = {
        'image1': ImageUploadField,
        'image2': ImageUploadField,
        'image3': ImageUploadField,
        'image4': ImageUploadField,
        'status': SelectField,
        'members': QuerySelectMultipleField
    }

    form_columns = [
        'title',
        'topic', 
        'overview',
        'status',
        'start_date',
        'end_date',
        'image1',
        'image2',
        'image3',
        'image4',
        'members'  
    ]

    form_args = {
        'image1': {
            'label': 'Project Image 1',
            'base_path': 'static/uploads/projects',
            'url_relative_path': 'uploads/projects/',
            'allowed_extensions': ['jpg', 'jpeg', 'png', 'gif'],
            'max_size': (1200, 800, False),
            'thumbnail_size': (150, 150, True),
            'validators': [validators.Optional()]
        },
        'image2': {
            'label': 'Project Image 2',
            'base_path': 'static/uploads/projects',
            'url_relative_path': 'uploads/projects/',
            'allowed_extensions': ['jpg', 'jpeg', 'png', 'gif'],
            'max_size': (1200, 800, False),
            'thumbnail_size': (150, 150, True),
            'validators': [validators.Optional()]
        },
        'image3': {
            'label': 'Project Image 3',
            'base_path': 'static/uploads/projects',
            'url_relative_path': 'uploads/projects/',
            'allowed_extensions': ['jpg', 'jpeg', 'png', 'gif'],
            'max_size': (1200, 800, False),
            'thumbnail_size': (150, 150, True),
            'validators': [validators.Optional()]
        },
        'image4': {
            'label': 'Project Image 4',
            'base_path': 'static/uploads/projects',
            'url_relative_path': 'uploads/projects/',
            'allowed_extensions': ['jpg', 'jpeg', 'png', 'gif'],
            'max_size': (1200, 800, False),
            'thumbnail_size': (150, 150, True),
            'validators': [validators.Optional()]
        },
        'status': {
            'choices': [('Ongoing', 'Ongoing'), ('Completed', 'Completed')],
            'coerce': str
        },
        'members': {
            'query_factory': lambda: Student.query.order_by(Student.name).all(),
            'get_label': 'name'  # Use string, not lambda
        }
    }

    def _list_thumbnail(view, context, model, name):
        img = getattr(model, name)
        if not img:
            return ''
        return f'<img src="/uploads/projects/{img}" width="75">'
    
    def _list_members(view, context, model, name):
        """Display member names in the list view"""
        if not model.members:
            return ''
        member_names = [m.name for m in model.members]
        return ', '.join(member_names[:3]) + ('...' if len(member_names) > 3 else '')

    column_formatters = {
        'image1': _list_thumbnail,
        'image2': _list_thumbnail,
        'image3': _list_thumbnail,
        'image4': _list_thumbnail,
        'members': _list_members,
    }

from wtforms import TextAreaField

class PublicationModelView(AuthenticatedModelView):
    column_list = ['title', 'authors', 'year', 'is_featured', 'citations']
    column_filters = ['year', 'is_featured']
    column_searchable_list = ['title', 'authors']
    
    form_overrides = {
        'bibtex': TextAreaField
    }
    
    form_args = {
        'bibtex': {
            'render_kw': {'rows': 10, 'placeholder': '@article{...}'}
        }
    }
    
    def on_model_change(self, form, model, is_created):
        model.parse_bibtex()
        super().on_model_change(form, model, is_created)

class LabInfoModelView(AuthenticatedModelView):
    can_create = False  
    can_delete = False  
    
    column_list = ['lab_name', 'lab_full_name', 'lab_email', 'lab_phone', 'lab_address']
    
    form_columns = [
        'lab_name', 
        'lab_full_name', 
        'mission', 
        'research_areas',
        'lab_email', 
        'lab_address', 
        'lab_phone'
    ]
    
    column_labels = {
        'lab_name': 'Lab Name',
        'lab_full_name': 'Full Name',
        'mission': 'Mission',
        'research_areas': 'Research Areas',
        'lab_email': 'Email',
        'lab_address': 'Address',
        'lab_phone': 'Phone'
    }
    
    form_widget_args = {
        'mission': {
            'rows': 5
        },
        'research_areas': {
            'rows': 5
        },
        'lab_address': {
            'rows': 3
        }
    }
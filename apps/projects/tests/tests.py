from django.test import TestCase
from django.urls import reverse
from django.forms.models import model_to_dict
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from apps.projects.serializers import TagSerializer, ProjectSerializer
from dateutil.parser import parse
from pathlib import Path
from apps.projects.models import (Tag, Project,
                                  ProjectFile, Task,
                                  Statuses, Priorities,
                                  )
from apps.user.models import Positions
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db.models import Q, F, Count, Max, Avg, ExpressionWrapper
from django.db.models.functions import ExtractWeekDay, ExtractIsoWeekDay
from datetime import datetime, timedelta
from faker import Faker
import random
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
import calendar
from django.core.paginator import Paginator
from django.core.files.uploadedfile import SimpleUploadedFile

class TestTag(APITestCase):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.create_db()

    def setUp(self):
        self.create_db()

    @staticmethod
    def create_db():
        now = timezone.now()
        _, last_day = calendar.monthrange(now.year, now.month)
        User = get_user_model()
        User.objects.create(first_name='da1', last_name='das', username='das1', email='helloy@yahoo.com')
        User.objects.create(first_name='da2', last_name='das2', username='das2')
        User.objects.create(first_name='da3', last_name='das3', username='das3')
        User.objects.create(first_name='da4', last_name='das4', username='das4')
        User.objects.create(first_name='da5', last_name='das5', username='das5')
        all_statuses = [choice.value for choice in Statuses]
        all_priorities = [choice.value for choice in Priorities]
        all_users = [user for user in User.objects.all()]
        Tag.objects.create(name='Разработка UI-кита и редизайн макета')
        Tag.objects.create(name='Настройка CI/CD, после сконфигурировать Docker')
        tag_1 = Tag(name='Backend')
        tag_2 = Tag(name='Frontend')
        tag_3 = Tag(name='Q&A')
        tag_4 = Tag(name='Design')
        tag_5 = Tag(name='DevOPS')
        Tag.objects.bulk_create([tag_1, tag_2, tag_3, tag_4, tag_5])
        fake = Faker()
        projects = [Project(name=fake.unique.word(),
                            description=fake.paragraph(nb_sentences=random.randint(2, 5)),
                            created_at=timezone.now())
                    for _ in range(10)]
        projects += [Project(name='New titanic project :D',
                          description='blablabla',
                             users=random.choice(User.objects.all())),
                  Project(name='Another titanic',
                          description='blabla')]
        Project.objects.bulk_create(projects)
        for project in Project.objects.filter(name='Another titanic'):
            for i in range(5):
                our_file = ProjectFile(name=f'file_{i}.txt')
                our_file.file.save(f'file_{i}.txt',
                                   ContentFile(fake.paragraph(nb_sentences=random.randint(2, 5))),
                                   save=True)
                our_file.save()
                project.files.add(our_file)
                project.save()
        for project in Project.objects.all():
            for tag in Tag.objects.all():
                task = Task.objects.create(name=fake.unique.word(),
                                    description=fake.paragraph(nb_sentences=random.randint(2, 5)),
                                    status=random.choice(all_statuses),
                                    priority=random.choice(all_priorities),
                                    due_date=fake.date_between_dates(timezone.make_aware(
                                        datetime(2026, 9, 1)),
                                        timezone.make_aware(datetime(2027, 4, 15))) ,
                                    project=project,
                                    assignee=random.choice(all_users)
                                    )
                task.tags.add(tag)
                task.save()
        another_task = Task.objects.create(name=fake.unique.word(),
                            description=fake.paragraph(nb_sentences=random.randint(2, 5)),
                            status=Statuses.NEW,
                            priority=Priorities.URGENT,
                            project=projects[0],
                            assignee=random.choice(all_users),
                            due_date=timezone.now() + timedelta(days=last_day)
                            )
        another_task.tags.add(tag_1)
        another_task.save()
        another_task = Task.objects.create(name=fake.unique.word(),
                                           description=fake.paragraph(nb_sentences=random.randint(2, 5)),
                                           status=Statuses.IN_PROGRESS,
                                           priority=Priorities.URGENT,
                                           project=projects[0],
                                           assignee=random.choice(all_users),
                                           due_date=timezone.now() + timedelta(days=last_day)
                                           )
        another_task.tags.add(tag_1)
        another_task.save()
        another_task = Task.objects.create(name=fake.unique.word(),
                                           description=fake.paragraph(nb_sentences=random.randint(2, 5)),
                                           status=Statuses.IN_PROGRESS,
                                           priority=Priorities.URGENT,
                                           project=projects[-2],
                                           assignee=random.choice(all_users),
                                           due_date=timezone.now() + timedelta(days=last_day),
                                           # created_at=timezone.now() - timedelta(weeks=5)
                                           )
        another_task.tags.add(tag_1)
        another_task.created_at = timezone.now() - timedelta(weeks=5)
        another_task.save()


    def test_tag_by_name(self):
        # self.create_db()
        self.assertEqual(Tag.objects.filter(name='Разработка UI-кита и редизайн макета').count(), 1)

    def test_tag_by_specific_tag(self):
        # self.create_db()
        self.assertEqual(Tag.objects.filter(name__icontains='de').count(), 2)

    def test_projects_by_date(self):
        # self.create_db()
        naive_date = datetime(year=2026, month=1, day=1)
        above_date = timezone.make_aware(naive_date)
        self.assertEqual(Project.objects.filter(created_at__gte=above_date).count(), Project.objects.all().count())

    def test_gte_or_contains_ti(self):
        # self.create_db()
        naive_date = datetime(year=2026, month=1, day=1)
        above_date = timezone.make_aware(naive_date)
        self.assertGreaterEqual(Project.objects.filter(Q(created_at__gte=above_date) & Q(name__icontains='ti')).count(), 2)

    def test_5_files_in_pr(self):
        # self.create_db()
        self.assertEqual(Project.objects.get(name='Another titanic').files.all().count(), 5)

    def test_st_new_pr_urg(self):
        # self.create_db()
        self.assertGreaterEqual(Task.objects.filter(status=Statuses.NEW, priority=Priorities.URGENT).count(), 1)

    def test_specific_task(self):
        task = Task.objects.all().first()
        task.status = Statuses.PENDING
        task.save()
        self.assertEqual(Task.objects.get(id = task.id).status, Statuses.PENDING)

    def test_st_pr_or_not_tag(self):
        self.assertGreaterEqual(Task.objects.filter(Q(status=Statuses.NEW, priority=Priorities.URGENT) | ~Q(tags__name__in=['Backend'])).count(), 1)

    def test_update_st_next_month(self):
        self.assertGreaterEqual(Task.objects.filter(due_date__month=timezone.now().month + 1).count(), 1)
        self.assertGreaterEqual(Task.objects.filter(due_date__month=timezone.now().month + 1).update(priority=Priorities.CRITICAL), 1)

    def test_task_due_date_by_week(self):
        self.assertEqual(Task.objects.all().update(due_date=F('due_date') + timedelta(weeks=1)), Task.objects.all().count())

    def test_not_assigned(self):
        self.assertEqual(Task.objects.filter(assignee__isnull=True).count(), 0)

    def test_task_with_tag(self):
        self.assertEqual(Task.objects.filter(tags__name='Frontend').count(), 12)

    def test_projects_by_period(self):
        now = timezone.now()
        creation_date = now - timedelta(days=7)
        # Search approach via ProjectFile table:
        # all_files_names = {file.name for file in ProjectFile.objects.filter(created_at__gte=creation_date)}
        # Search approach via Project table:
        all_files_names = {file.name for project in Project.objects.filter(created_at__gte=creation_date) for file in project.files.all()}
        self.assertGreaterEqual(Project.objects.filter(files__name__in=all_files_names).count(), 1)

    def test_new_status(self):
        self.assertGreaterEqual(Task.objects.filter(status=Statuses.NEW).update(status=Statuses.IN_PROGRESS), 1)

    def test_mass_due_date(self):
        self.assertGreaterEqual(Task.objects.filter(status=Statuses.IN_PROGRESS).update(due_date=F('due_date') + timedelta(days=3)), 1)

    def test_mass_filter_by_date(self):
        yesterday = timezone.now() - timedelta(days=1)
        projects_many_files = Project.objects.annotate(files_count=Count('files')).filter(created_at__gt=yesterday, files_count__gte=5).count()
        self.assertGreaterEqual(projects_many_files, 1)
        print(projects_many_files)
        projects_max_files = Project.objects.annotate(max_files = Max('files')).all()
        print(projects_max_files)

    def test_critical_or_urgent(self):
        cur_date = timezone.now()
        _, last_day = calendar.monthrange(cur_date.year, cur_date.month)
        self.assertGreaterEqual(Task.objects.filter(Q(priority=Priorities.CRITICAL) | Q(priority=Priorities.URGENT) & Q(due_date__day__range =[cur_date.day, last_day])).count(), 1)

    def test_not_in_status(self):
        self.assertGreaterEqual(Task.objects.filter(~Q(status__in=[Statuses.PENDING, Statuses.CLOSED])).count(), 1)

    def test_upd_priority(self):
        one_month_ago = timezone.now() - timedelta(weeks=5)
        self.assertEqual(Task.objects.filter(project__name='New titanic project :D', created_at__lt=one_month_ago).update(priority=Priorities.CRITICAL), 1)

    def test_current_month(self):
        cur_date = timezone.now()
        for project in Project.objects.filter(created_at__gte=datetime(cur_date.year, cur_date.month, 1)):
            self.assertEqual(project.created_at.month, timezone.now().month)

    def test_files_per_week_day(self):
        cur_day = timezone.now().isoweekday()
        project_files = ProjectFile.objects.annotate(day_of_week=ExtractIsoWeekDay('created_at')).filter(day_of_week=cur_day)
        self.assertTrue(project_files.exists())
        for project_file in project_files:
            self.assertEqual(project_file.created_at.isoweekday(), cur_day)
            self.assertEqual(project_file.day_of_week, cur_day)

    def test_projects_all(self):
        self.assertGreater(Project.objects.all().count(), 1)

    def test_count_files_by_project(self):
        # self.assertEqual(ProjectFile.objects.values('projects__name').annotate(files_count=Count('id')).
        #                  values('projects__name', 'files_count').count(), 1)
        for project in Project.objects.values('name').annotate(files_count=Count('files__id')).values('name', 'files_count'):
            print(project['name'], project['files_count'])
            self.assertEqual(project['files_count'], Project.objects.get(name=project['name']).files.count())

    def test_avg_avg_tasks_quan(self):
        self.assertEqual(Project.objects.annotate(tasks_count=Count('tasks__id')).aggregate(avg_tasks=Avg('tasks_count'))['avg_tasks'], 7.25)

    def test_tasks_per_user(self):
        User = get_user_model()
        for user in User.objects.values('username').annotate(tasks_count=Count('tasks__id')).values('username', 'tasks_count'):
            print(f'Username: {user['username']}, tasks count: {user['tasks_count']}')
            self.assertEqual(user['tasks_count'], User.objects.get(username=user['username']).tasks.count())

    def test_sort_tasks(self):
        for task in Task.objects.order_by('priority', 'due_date').values('name', 'priority', 'due_date'):
            print(task)
            assert 'name' in task
            assert 'due_date' in task
            assert task['due_date'] is not None

    def test_sort_users_by_tasks(self):
        User = get_user_model()
        for user in User.objects.values('username').annotate(tasks_count=Count('tasks__id')
                                                 ).order_by('-tasks_count').values('username', 'tasks_count'):
            print(user)

    def test_all_tasks_with_pagination(self):
        all_tasks = Task.objects.all().values('name', 'status', 'priority', 'assignee__username').order_by('id')
        pagination = Paginator(all_tasks, per_page=10)
        # for page_number in range(1, pagination.num_pages + 1):
        for page_number in pagination.page_range:
            page = pagination.get_page(page_number)
            print(page)
            for task in page:
                print(task)
            print("-" * 50)

    def test_tag_api(self):
        response = self.client.get(reverse('tag-list-view'))
        assert len(response.data) >= 1

    def test_tag_api(self):
        tag_name = {'name': 'helloy'}
        response = self.client.post(reverse('tag-list-view'), data=tag_name)
        assert response.data['name'] == 'helloy'

    def test_detail_api(self):
        our_tag = Tag.objects.all().first()
        response = self.client.get(reverse('tag-detail-view', args=[our_tag.id]), format='json')
        assert len(response.data) > 1
        assert 'id' in response.data

    def test_detail_api_patch(self, method='patch'):
        our_tag = Tag.objects.first()
        tag_id = str(our_tag.id)
        tag_name = {'name': 'tony'}
        if method == 'patch':
            response = self.client.patch(reverse('tag-detail-view', args=[our_tag.id]), data=tag_name, format='json')
        elif method == 'put':
            response = self.client.put(reverse('tag-detail-view', args=[our_tag.id]), data=tag_name, format='json')
        else:
            raise ValueError('method must be either put or patch!')
        self.assertEqual(response.status_code, 200)
        our_tag.refresh_from_db()
        # our_tag = Tag.objects.get(id=our_tag.id)
        # assert our_tag.name == 'tony'
        serialized = TagSerializer(our_tag).data
        self.assertEqual({k: v for k, v in serialized.items() if k in {'id', 'name'}},
                         {'id': tag_id, 'name': 'tony'})

    def test_detail_api_put(self):
        return self.test_detail_api_patch(method='put')

    def test_delete_tag_api(self):
        our_tag_id = Tag.objects.first().id
        response = self.client.delete(reverse('tag-detail-view', args=[our_tag_id]), format='json')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Tag.objects.filter(id=our_tag_id).exists())

    def test_project_get_params(self):
        response = self.client.get(reverse('project-list-view'),
        query_params={'date_from': timezone.now().strftime('%d-%m-%Y'), 'date_to': timezone.now().strftime('%d-%m-%Y')}, format='json')
        for item in response.data:
            item.pop('count_of_files', None)
            project = Project(**item)
            self.assertEqual(parse(project.created_at).day, timezone.now().day)
            self.assertEqual(parse(project.created_at).month, timezone.now().month)
            self.assertEqual(parse(project.created_at).year, timezone.now().year)

    def test_upload_file(self):
        project_id = Project.objects.first().id
        # file_path = Path().resolve().joinpath('media', 'projects', 'ls4_combined.py')
        # file_path = Path().resolve() / 'media' / 'projects' / 'ls4_combined.py' # Not stable iteration
        file_path = Path(__file__).resolve().parents[3] / 'media' / 'projects' / 'ls4_combined.py'
        with open(file_path, 'rb') as fl:
            response = self.client.post(reverse('file-list-view'), data={
                "name": "hey :DDD",
                "file": fl,
                "projects": project_id
            }, format='multipart')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data['name'], 'hey :DDD')

    def test_file_size_too_big_generated(self):
        project_id = Project.objects.first().id
        our_content = b"0" * int(2.5 * 1024 * 1024)
        big_data = SimpleUploadedFile('too_big_file_xD.txt', content=our_content, content_type='text/plain')
        response = self.client.post(reverse('file-list-view'), data={
            "name": "Big file x)",
            "file": big_data,
            "projects": project_id
        }, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertIn('File size too big', response.data['file'])

    def test_file_size_too_big(self):
        project_id = Project.objects.first().id
        file_path = Path(__file__).resolve().parent.parent.parent.parent.joinpath('media', 'projects', 'valid_passwords.txt')
        with open(file_path, 'rb') as fl:
            response = self.client.post(reverse('file-list-view'), data={
                "name": "Big passwords file :)",
                "file": fl,
                "projects": project_id
            }, format='multipart')
            self.assertEqual(response.status_code, 400)
            self.assertIn('File size too big', response.data['file'])

    def test_file_extension_error(self):
        project_id = Project.objects.first().id
        file_path = Path(__file__).resolve().parent.parent.parent.parent.joinpath('media', 'projects', 'terraform-test2.7z')
        with open(file_path, 'rb') as fl:
            response = self.client.post(reverse('file-list-view'), data={
                "name": "Not specified file extension :)",
                "file": fl,
                "projects": project_id
            }, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertIn('This extension is not allowed!', response.data['file'])

    def test_project_files_count(self):
        response = self.client.get(reverse('project-list-view'))
        self.assertEqual(response.status_code, 200)
        for project in response.data:
            self.assertIn('count_of_files', project)

    def test_create_task_by_name(self):
        project = Project.objects.first()
        fake = Faker()
        User = get_user_model()
        task = {'name': 'fake.unique.word()',
                'description': fake.paragraph(nb_sentences=random.randint(2, 5)),
                'status': random.choice(Statuses.values),
                'priority': random.choice(Priorities.values),
                'due_date': fake.date_between_dates(timezone.make_aware(
                    datetime(2026, 9, 1)),
                    timezone.make_aware(datetime(2027, 4, 15))) ,
                'project': project.name,
                'assignee': User.objects.filter(~Q(email='')).first().email}
        response = self.client.post(reverse('task-post-view'), data=task, format='json')
        self.assertEqual(response.status_code, 201)

    def test_task_update_delete(self):
        task = Task.objects.last()
        response = self.client.get(reverse('task-detail-view', args=[task.id]))
        self.assertEqual(response.status_code, 200)
        data = {'name': 'test_patch'}
        response = self.client.patch(reverse('task-detail-view', args=[task.id]), data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'test_patch')
        response = self.client.delete(reverse('task-detail-view', args=[task.id]))
        self.assertEqual(response.status_code, 204)

    def test_get_user(self):
        response = self.client.get(reverse('user-list-view'), query_params={'project': 'New titanic project :D'})
        self.assertEqual(response.status_code, 200)
        for user in response.data:
            self.assertEqual(user['project'][0]['name'], 'New titanic project :D')

    def test_post_user(self):
        data = {'first_name': 'dadjasndjkasknj', 'last_name': 'dasdladajsjds', 'username': 'das56', 'position': random.choice(Positions.values),
                'email': 'helloworld@woryahoo.com', 'password': 'super_secure_12345', 're_password': 'super_secure_12345'}
        response = self.client.post(reverse('user-list-view'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_post_task_with_assignee(self):
        project = random.choice(Project.objects.all())
        fake = Faker()
        User = get_user_model()
        data = {'name': 'fake.unique.word()',
                'description': fake.paragraph(nb_sentences=random.randint(2, 5)),
                'status': random.choice(Statuses.values),
                'priority': random.choice(Priorities.values),
                'due_date': fake.date_between_dates(timezone.make_aware(
                    datetime(2026, 9, 1)),
                    timezone.make_aware(datetime(2027, 4, 15))) ,
                'project': project.name,
                'assignee': User.objects.filter(~Q(email='')).first().email}
        response = self.client.post(reverse('task-post-view'), data=data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_project_file(self):
        project_file = ProjectFile.objects.first()
        response = self.client.get(reverse('file-retrieve-view', args=[project_file.id]))
        self.assertEqual(response.status_code, 200)
        print(str(b''.join(response.streaming_content)))
        self.assertEqual(project_file.name, response.filename)

    def test_get_project_file_in_db_negative(self):
        from uuid import UUID
        import uuid
        # response = self.client.get(reverse('file-retrieve-view', args=[UUID('1e096a4c-9596-0000-a690-93a5c7dc600d')]))
        response = self.client.get(reverse('file-retrieve-view', args=[uuid.uuid4()]))
        self.assertEqual(response.status_code, 404)
        # self.assertIn('No ProjectFile matches the given query.', response.data['detail'])
        self.assertIn("The requested file record does not exist", response.data['detail'])

    def test_get_project_file_from_storage_negative(self):
        pr_file = ProjectFile.objects.create(name=f'file_123.txt')
        pr_file.file.name = 'projects/non_existing_file.txt'
        pr_file.save()
        response = self.client.get(reverse('file-retrieve-view', args=[pr_file.id]))
        self.assertEqual(response.status_code, 404)
        # self.assertIn('No ProjectFile matches the given query.', response.data['detail'])
        self.assertIn("The file asset is missing from storage", response.data['detail'])


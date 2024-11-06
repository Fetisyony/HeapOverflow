from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from random import sample, choice

POPULAR_TAGS = ["python", "ruby", "linux", "kotlin", "arch", "c++", "android", "ios", "django", "flask"]
tags = POPULAR_TAGS + ["fastapi", "sql", "nosql", "postgresql", "mysql", "sqlite"]

USERS_DATABASE = [
    {
        "name" : "Ryan Gosling",
        "avatar" : "img/AnswerProfile1.jpg",
    },
    {
        "name" : "Oscar Isaac",
        "avatar" : "img/AnswerProfile2.png",
    },
    {
        "name" : "Peter",
        "avatar" : "img/AnswerProfile3.png",
    },
    {
        "name" : "Carrey Mulligan",
        "avatar" : "img/Avatar.jpg",
    },
    {
        "name" : "Christina Hendricks",
        "avatar" : "img/AnswerProfile2.png",
    }
]

QUESTIONS = [
    {
        'title': 'Why is processing a sorted array faster than processing an unsorted array?',
        'id': 1,
        'text': 'In C++, sorting the data before a timed region makes the primary loop approximately 6 times faster. Sorting helps optimize the cache locality and reduce branch mispredictions, which results in faster processing of sorted arrays. The algorithm and data structure choices play an important role in optimizing the runtime.',
        'tags': ["java", "performance", "cpu-architecture"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'How do I undo the most recent local commits in Git?',
        'id': 2,
        'text': 'If you accidentally committed the wrong files in Git, but have not yet pushed the commit to the server, you can use `git reset --soft HEAD~1` to undo the most recent commit while keeping the changes in your working directory. Alternatively, `git reset --hard HEAD~1` will discard the changes completely.',
        'tags': ["git", "version-control", "git-commit", "undo"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'How do I delete a Git branch locally and remotely?',
        'id': 3,
        'text': 'To delete a branch locally, use `git branch -d <branch-name>`. If you want to delete it remotely, use `git push origin --delete <branch-name>`. Be sure to check if the branch has been merged to avoid losing important changes.',
        'tags': ["git", "version-control", "git-branch", "git-push"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'What is the difference between "git pull" and "git fetch"?',
        'id': 4,
        'text': 'The key difference is that `git fetch` downloads the latest commits from the remote repository but does not merge them into your current working branch, whereas `git pull` automatically fetches the changes and merges them with your local branch. It is often safer to use `git fetch` to review changes before merging.',
        'tags': ["git", "version-control", "git-pull", "git-fetch"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'What does the "yield" keyword do in Python?',
        'id': 5,
        'text': 'The `yield` keyword in Python is used to pause the function and return a value to the caller, while saving the state of the function. This allows the function to be resumed later, making it an ideal tool for creating iterators and generators.',
        'tags': ["python", "iterator", "generator", "yield"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'How can I remove a specific item from an array in JavaScript?',
        'id': 6,
        'text': 'In JavaScript, you can remove an item from an array using the `splice` method. For example, `array.splice(index, 1)` will remove the element at the specified index. Alternatively, you can use `filter()` to remove all occurrences of a specific value.',
        'tags': ["javascript", "arrays"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'How can I rename a local Git branch?',
        'id': 7,
        'text': 'To rename a local Git branch that has not yet been pushed to a remote repository, use the command `git branch -m old-branch-name new-branch-name`. If you are currently on the branch you want to rename, simply use `git branch -m new-branch-name`.',
        'tags': ["git", "version-control", "git-branch"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'Which JSON content type do I use?',
        'id': 8,
        'text': 'The recommended content type for JSON is `application/json`. However, some systems might use other content types like `text/javascript` or `application/x-javascript`. Always check the documentation of the API you are working with to ensure compatibility.',
        'tags': ["json", "mime-types", "content-type"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'How do I undo "git add" before commit?',
        'id': 9,
        'text': 'If you added files to the staging area using `git add` but have not yet committed them, you can unstage the files with `git reset <file-name>`. To unstage all files, use `git reset` without specifying a file name.',
        'tags': ["git", "undo", "git-add"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'What is the "-->" operator in C/C++?',
        'id': 10,
        'text': 'The `-->` operator in C and C++ is not a standard operator, but it can appear in specific contexts like preprocessor macros or custom operator overloading. It is often used in combination with certain compiler extensions or in poorly documented or non-standard codebases.',
        'tags': ["c++", "operators" "standards-compliance"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'How do I force "git pull" to overwrite local files?',
        'id': 11,
        'text': 'To force a `git pull` to overwrite local files, you can use `git fetch` followed by `git reset --hard origin/<branch-name>`. This will discard all local changes and forcefully align your local branch with the remote branch.',
        'tags': ["git", "version-control", "git-pull", "git-fetch"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'Can comments be used in JSON?',
        'id': 12,
        'text': 'According to the official JSON specification, comments are not allowed in JSON files. However, some parsers may support comments as an extension, but it is not a best practice to rely on this for production systems.',
        'tags': ["json", "comments"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'What and where are the stack and heap?',
        'id': 13,
        'text': 'The stack and heap are two areas of memory in a program. The stack is used for static memory allocation, such as local variables and function calls, whereas the heap is used for dynamic memory allocation, such as objects created during runtime.',
        'tags': ["data-structures", "stack-memory", "heap-memory"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'Why does HTML think "chucknorris" is a color?',
        'id': 14,
        'text': 'In HTML, certain non-standard strings can be interpreted as colors, including the string "chucknorris". This behavior occurs because the HTML specification includes a set of predefined color names, and "chucknorris" is a quirky, non-standard addition to that list in some browsers.',
        'tags': ["html", "browser", "background-color"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'How do I check out a remote Git branch?',
        'id': 15,
        'text': 'To check out a remote branch in Git, use the command `git checkout -b <branch-name> origin/<branch-name>`. This will create a local tracking branch and switch to it, synchronizing with the remote branch.',
        'tags': ["git", "version-control", "git-branch"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'How do I remove a property from a JavaScript object?',
        'id': 16,
        'text': 'In JavaScript, you can remove a property from an object using the `delete` operator. For example, `delete myObject.propertyName` will remove the specified property from the object.',
        'tags': ["javascript", "object", "properties"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'What are metaclasses in Python?',
        'id': 17,
        'text': 'A metaclass in Python is a class that defines how other classes are constructed. It is used to modify the creation of classes themselves, allowing for customization of class behavior and attributes at the time of their creation.',
        'tags': ["python", "oop", "python-datamodel"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'How to check whether a string contains a substring in JavaScript?',
        'id': 18,
        'text': 'In JavaScript, you can check if a string contains a substring using the `includes()` method. For example, `"Hello World".includes("World")` will return `true`.',
        'tags': ["javascript", "string", "substring", "string-matching"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'How do I check whether a file exists without exceptions?',
        'id': 19,
        'text': 'In Python, you can check if a file exists without using exceptions by using `os.path.exists()` or `pathlib.Path.exists()`. These methods return `True` if the file exists, and `False` otherwise.',
        'tags': ["python", "file", "file-exists"],
        'author': choice(USERS_DATABASE),
    },
    {
        'title': 'How do I merge two dictionaries in a single expression in Python?',
        'id': 0,
        'text': 'In Python, you can merge two dictionaries using the `update()` method or using the `{**dict1, **dict2}` syntax. The second approach is a more modern and concise way of merging dictionaries in one expression.',
        'tags': ["python", "dictionary", "merge"],
        'author': choice(USERS_DATABASE),
    },
]

POPULAR_TAGS = ["python", "ruby", "linux", "kotlin", "arch", "c++", "android", "ios"]
TOP_USER_ID = [0, 1, 2]

tags = []

def index(request):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 4)
    page = paginator.page(page_number)

    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="index.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

def hot(request):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_number)

    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="hot.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

def settings(request):
    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="settings.html",
        context={
            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

def question(request, question_id):
    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="question.html",
        context={
            'question': QUESTIONS[question_id],
            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

def askQuestion(request):
    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="ask.html",
        context={
            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

def tag(request, tag_name):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_number)

    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="tag.html",
        context={
            'page_obj': page,
            'questions': page.object_list,

            'tag_name': tag_name,

            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

def register(request):
    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="register.html",
        context={
            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

def login(request):
    top_users_list = [USERS_DATABASE[i] for i in TOP_USER_ID]

    return render(
        request,
        template_name="login.html",
        context={
            'popular_tags': POPULAR_TAGS,
            'top_users': top_users_list
        }
    )

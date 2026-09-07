def has_contact(book,name):
    print(name in book) 

book = {"张三": {"phone": "123456789", "email": "zhangsan@example.com"}}

has_contact(book, "张三")  # True
has_contact(book, "李四")  # False
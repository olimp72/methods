# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies1507

    def process_item(self, item, spider):
        item['salary'] = self.process_salary(item['salary'])

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, salary):
        salary_edit = []
        for sal in salary:
            if sal != ' ':
                if sal[0].isdigit():
                    salary_edit.append(int(''.join(sal.split())))
                else:
                    salary_edit.append(sal.strip())
        if 'от' in salary_edit and 'до' in salary_edit:
            min_salary = salary_edit[1]
            max_salary = salary_edit[3]
            cur_salary = salary_edit[4]
        elif 'от' in salary_edit:
            min_salary = salary_edit[1]
            max_salary = None
            cur_salary = salary_edit[2]
        elif 'до' in salary_edit:
            min_salary = None
            max_salary = salary_edit[1]
            cur_salary = salary_edit[2]
        else:
            min_salary = None
            max_salary = None
            cur_salary = None
        return min_salary, max_salary, cur_salary

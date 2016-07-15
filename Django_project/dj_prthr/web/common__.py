#encoding:utf-8

from django.utils.safestring import mark_safe

def try_int(arg, default):
  try:
    arg = int(arg)
  except Exception, e:
    arg = default
  return arg

class PageInfo(object):
  def __init__(self, current, total_item, per_item = 5):
    self.__current = current
    self.__per_item = per_item
    self.__total_item = total_item

  def From(self):
    return (self.__current-1) * self.__per_item

  def To(self):
    return self.__current * self.__per_item

  def total_page(self):
    result = divmod(self.__total_item, self.__per_item)
    if result[1] == 0:
      return result[0]
    else:
      return result[0] + 1

def customPage(baseurl, current_page, total_page):
  per_page = 11
  begin = 0
  end = 0

  if total_page <= 11:
    begin = 0
    end = total_page
  else:
    if current_page > 5:
      begin = current_page - 5
      end = current_page + 5
      if end > total_page:
        end = total_page
    else:
      begin = 0
      end = 11

  page_list = []
  if current_page <= 1:
    #first = "<a href='' class='disabled'>首页</a> "
    first = ''
  else:
    first = "<a href='%s%d/'>首页</a> " %(baseurl, 1)
  page_list.append(first)

  if current_page <= 1:
    #prev = "<a href='' class='disabled'>上一页</a> "
    prev = ''
  else:
    prev = "<a href='%s%d/'>上一页</a> " %(baseurl, current_page - 1)
  page_list.append(prev)

  for i in range(begin+1, end+1):
    if i == current_page:
      temp = "<a href='%s%d/' class='selected'><b>%d</b></a> " %(baseurl, i, i)
    else:
      temp = "<a href='%s%d/'>%d</a> " %(baseurl, i, i)
    page_list.append(temp)

  if current_page >= total_page:
    #next = "<a href='' class='disabled'>下一页</a> "
    next = ''
  else:
    next = "<a href='%s%d/'>下一页</a> " %(baseurl, current_page+1)
  page_list.append(next)

  if current_page >= total_page:
    #last = "<a href='' class='disabled'>尾页</a>"
    last = ''
  else:
    last = "<a href='%s%d/'>尾页</a>" %(baseurl, total_page)
  page_list.append(last)

  result = ''.join(page_list)
  return mark_safe(result)

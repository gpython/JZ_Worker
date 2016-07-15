#encoding:utf-8

from django.utils.safestring import mark_safe

def try_int(arg, default):
  try:
    arg = int(arg)
  except Exception, e:
    arg = default
  return arg

class PageInfo(object):
  def __init__(self, current, total_item, per_item=5):
    self._current = current
    self._per_item = per_item
    self._total_item = total_item

  def From(self):
    return (self._current - 1) * self._per_item

  def To(self):
    return self._current * self._per_item

  def total_page(self):
    result = divmod(self._total_item, self._per_item)
    if result[1] == 0:
      return result[0]
    else:
      return result[0] + 1

def customPage(baseurl, current_page, total_page, per_page = 11):

  if total_page < per_page:
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
      end = per_page

  page_list = []

  if current_page <= 1:
    first = ''
    prev = ''
  else:
    first = "<a href='%s%d/'>首页</a> " %(baseurl, 1)
    prev = "<a href='%s%d/'>上一页</a> " %(baseurl, current_page - 1)
  page_list.append(first)
  page_list.append(prev)

  for i in range(begin+1, end+1):
    if current_page == i:
      temp = "<a href='%s%d/' class='selected'><b>%d</b></a> " %(baseurl, i, i)
    else:
      temp = "<a href='%s%d/'>%d</a> " %(baseurl, i, i)
    page_list.append(temp)

  if current_page >= total_page:
    next_page = ''
    last = ''
  else:
    next_page = "<a href='%s%d/'>下一页</a> " %(baseurl, current_page+1)
    last = "<a href='%s%d/'>尾页</a>" %(baseurl, total_page)
  page_list.append(next_page)
  page_list.append(last)

  return mark_safe(''.join(page_list))



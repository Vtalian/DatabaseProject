class Paging:
    # page_num为每页显示的数量，max_page_num为每页显示的总页码数
    def __init__(self, request, lengths, page_num=10, max_page_num=7):
        # 首先进行异常错误处理，比如：.../?page=-5等
        try:
            # 获取url中的page值，并将默认值设置为1
            page = int(request.GET.get('page', 1))
            # print(page, type(page))
            if page < 1:
                page = 1
        except Exception:
            page = 1
        # print(page)

        # 每页显示的数量
        # page_num = 7

        # 计算总页码数
        # divmod为len(user_list) / page_num，整数为total_num，余数为remainder
        total_num, remainder = divmod(lengths, page_num)
        if remainder != 0:
            total_num += 1
        # print(total_num)

        # 每页显示的总页码数
        # max_page_num = 7

        # 每页显示总页码数一半数
        half_num = max_page_num // 2
        # 实际总页码数 < 页面总页码数
        if total_num < max_page_num:
            # 页码起始值
            page_start = 1
            # 页码终止值
            page_end = total_num
        # 实际总页码数 > 页面总页码数
        else:
            # 处理左边极值
            if page - half_num < 1:
                page_start = 1
                page_end = max_page_num
            # 处理右边极值
            elif page + half_num > total_num:
                page_start = total_num - max_page_num + 1
                page_end = total_num
            else:
                page_start = page - half_num
                page_end = page + half_num

        html_list = ['<nav aria-label="Page navigation"><ul class="pagination justify-content-center">']

        if page == 1:
            html_list.append(
                '<li class="disabled"><a class="page-link" href="#" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            html_list.append(
                '<li class="page-item"><a class="page-link" href="?page=%s" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>' % (
                            page - 1))

        for i in range(page_start, page_end + 1):
            if page == i:
                html_list.append('<li class="active"><a class="page-link" href="?page=%s">%s</a></li>' % (i, i))
            else:
                html_list.append('<li class="page-item"><a class="page-link" href="?page=%s">%s</a></li>' % (i, i))

        if page == total_num:
            html_list.append(
                '<li class="disabled"><a class="page-link" href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            html_list.append(
                '<li class="page-item"><a class="page-link" href="?page=%s" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>' % (
                            page + 1))

        html_list.append('</ul></nav>')

        self.html_list = ''.join(html_list)

        # 起始
        # start = 0
        self.start = (page - 1) * page_num
        # 终止
        # end = 7
        self.end = page * page_num


# 要调用的值

"""
self.start
self.end
self.html_list
"""

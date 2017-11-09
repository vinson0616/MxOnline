# coding:utf-8
__authoer__ = 'Vinson'
__date__ = '11/9/2017 05:42 PM'

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


# excel 导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    # 只有为true，才加载这个插件
    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self,context,nodes):
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html',context_instance=context))


xadmin.site.register_plugin(ListImportExcelPlugin,ListAdminView)
# -*- coding: utf-8 -*-

from django.http.response import Http404
from django.views.generic import TemplateView
from graph.models import GraphModel
from graph.utils import get_model_from_path
from account.models import Node


class ModelListGraphsView(TemplateView):
    template_name = 'graph/index.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            raise Http404
        return super(ModelListGraphsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModelListGraphsView, self).get_context_data(**kwargs)
        context['graphs'] = GraphModel.objects.all()
        return context


class ModelGraphView(TemplateView):
    template_name = 'graph/tree.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            raise Http404
        return super(ModelGraphView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModelGraphView, self).get_context_data(**kwargs)
        # model = get_model_from_path(self.kwargs['modpath'])
        root_node_pk = self.kwargs['pk']
        root_node = Node.objects.get(pk=root_node_pk)
        nodes = root_node.get_descendants(include_self=True)[:20]

        context['nodes'] = nodes
        context['root_id'] = root_node_pk
        context['total_count'] = root_node.children.count()
        return context


class ModelGraphInlineView(ModelGraphView):
    template_name = 'graph/tree_inline.html'



from manim import *
from datascience import *
import numpy as np
from helpers import *

dummy1 = Table().with_columns('Index',np.arange(0,5),
                              'Protein',make_array(3,3.5,2,3.8,3.5),
                              'Carbs',make_array(6,7.5,4,8,9),
                              'Spice Level',make_array('Hot','Hot','Mild','Hot','Mild'))

class AnimateWhere(Scene):
    def construct(self):
        before = dummy1
        after = dummy1.where('Protein',are.above(3))
        anim = WhereAnimation(self,before,after)
        anim.animate('Protein')
    
class AnimateSort(Scene):
    def construct(self):
        before = dummy1
        after = dummy1.sort('Carbs',descending=True)
        anim = SortAnimation(self,before,after)
        anim.animate('Carbs')
    
class AnimateSelectSingle(Scene):
    def construct(self):
        before = dummy1
        after = dummy1.select('Carbs')
        anim = SelectAnimation(self,before,after)
        anim.animate('Carbs')

class AnimateSelectMultiple(Scene):
    def construct(self):
        before = dummy1
        after = dummy1.select('Carbs','Protein')
        anim = SelectAnimation(self,before,after)
        anim.animate(['Protein','Carbs'])

class AnimateDropMultiple(Scene):
    def construct(self):
        before = dummy1
        after = dummy1.drop('Carbs','Protein')
        anim = DropAnimation(self,before,after)
        anim.animate(['Protein','Carbs'])

class AnimateTake(Scene):
    def construct(self):
        before = dummy1
        after = dummy1.take(np.arange(1,3))
        anim = TakeAnimation(self,before,after)
        anim.animate()

class AnimateGroup(Scene):
    def construct(self):
        before = dummy1
        after = dummy1.group('Protein')
        anim = GroupAnimation(self,before,after)
        anim.animate('Protein')


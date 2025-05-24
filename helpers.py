from manim import *
from datascience import *
from datascience import Table as DataTable


def to_manim(scene:Scene,table: DataTable, **kwargs) -> MathTable:
    """
    Converts a Data 8 Table into a Manim MathTable.
    kwargs are passed to MathTable optional arguments.
    """
    rows = table.rows
    cols = table.labels
    
    manim_data = [list(map(str, cols))] + [list(map(str, row)) for row in rows]
    math_table = MathTable(manim_data,include_outer_lines=True, **kwargs,line_config={"color": BLACK},element_to_mobject=lambda text: Text(text, color=BLACK))
    num_rows = len(manim_data)
    num_cols = len(manim_data[0])
    backgrounds = []

    
            
    return math_table

class TableAnimation:
    def __init__(self, scene:Scene, source: DataTable, target: DataTable):
        self.scene = scene
        self.source = source
        self.target = target
        self.m_source = to_manim(scene,source)
        self.m_target = to_manim(scene,target)
        self.match_map = self.get_match_map()
        self.scene.camera.background_color = '#99C7F1'

    def get_match_map(self):
        # Generates match_map from source and target tables
        match_map = {}
        for src_idx, src_row in enumerate(self.source.rows):
            for tgt_idx, tgt_row in enumerate(self.target.rows):
                if src_row == tgt_row and tgt_idx not in match_map.values():
                    match_map[src_idx] = tgt_idx
                    break
        return match_map

    def highlight_column_header(self, col_idx, color):
        label_cell = self.m_source.get_rows()[0][col_idx]
        self.scene.play(Create(SurroundingRectangle(label_cell, color=color)))
        self.scene.wait(0.75)
    
    def set_up_source(self,scl=0.4):
        # Centers tables, scales to correct size, fades in source table
        self.m_source.scale(scl)
        self.m_target.scale(scl)
        tables = VGroup(self.m_source, self.m_target).arrange(RIGHT, buff=1)
        tables.move_to(ORIGIN)
        self.scene.play(FadeIn(self.m_source,run_time=2))
        self.scene.wait()
    
    def set_up_target(self):
        for i in range(1, self.target.num_rows + 1):
            self.m_target.get_rows()[i].set_opacity(0)
        self.scene.play(FadeIn(self.m_target),run_time=1)
    
    def remove_highlighted_cell(self,table: MathTable, row: int, col: int):
        cell = table.get_cell((row, col))
        for mobj in list(cell.submobjects):
            if isinstance(mobj, Rectangle) and mobj.fill_opacity > 0.1:
                self.scene.remove(mobj)
                cell.remove(mobj)

    def animate(self):
        raise NotImplementedError("Subclasses must implement animate function")

class WhereAnimation(TableAnimation):
    def animate(self,col:str):
        # e.g. -> animate("Protein") -> animation for filtering where "Protein" column has specific value
        # Highlight column
        self.set_up_source()
        col_idx = self.source.labels.index(col)
        self.highlight_column_header(col_idx,RED)

        # Highlight column cells
        for src_idx in range(self.source.num_rows):
            color = GREEN if src_idx in self.match_map else RED
            self.m_source.add_highlighted_cell((src_idx + 2, col_idx + 1), color=color)
            self.scene.wait(0.5)

        # Move matching rows
        self.set_up_target()
        for src_idx, tgt_idx in self.match_map.items():
            src_row = self.m_source.get_rows()[src_idx + 1]
            tgt_row = self.m_target.get_rows()[tgt_idx + 1]
            row_copy = src_row.copy()
            row_copy.move_to(tgt_row)
            self.scene.play(TransformFromCopy(src_row, row_copy))
            tgt_row.set_opacity(1)
            self.scene.wait()

class SortAnimation(TableAnimation):
    def animate(self,col_name:str):
        # e.g. -> animate("Carbs") -> animation for sorting on the "Carbs" column
        # Highlight column
        self.set_up_source()
        col_idx = self.source.labels.index(col_name)
        self.highlight_column_header(col_idx,RED) # What this do?

        # Highlight column cells 
        for src_idx, _ in enumerate(self.source.rows):
            self.remove_highlighted_cell(self.m_source,src_idx+2, col_idx+1)
            self.m_source.add_highlighted_cell((src_idx + 2, col_idx+1), color='#FEC34B')
            self.scene.wait(0.15)
        
        # Move matching cells
        self.set_up_target()
        for tgt_idx, tgt_row in enumerate(self.target.rows):
            src_idx = next(i for i, row in enumerate(self.source.rows) if row == tgt_row)

            source_row = self.m_source.get_rows()[src_idx + 1]
            target_row = self.m_target.get_rows()[tgt_idx + 1]

            row_copy = source_row.copy()
            row_copy.move_to(target_row)

            self.scene.play(TransformFromCopy(source_row, row_copy))
            target_row.set_opacity(0.5)
            self.scene.wait(0.7)
        
        # Highlight sorted cells
        col_idx = self.target.labels.index(col_name)
        for tgt_idx, _ in enumerate(self.target.rows):
            self.remove_highlighted_cell(self.m_target,tgt_idx + 2, col_idx+1)
            self.m_target.add_highlighted_cell((tgt_idx + 2, col_idx+1), color='#FEC34B')
            self.scene.wait(0.15)

class SelectAnimation(TableAnimation):
    def animate(self,cols):
        # Makes single column a list with one entry
        if isinstance(cols, str):
            cols = [cols]
        self.set_up_source()
        for col_name in cols:
            col_idx = self.source.labels.index(col_name)
            self.highlight_column_header(col_idx,RED)

            # Highlight column cells 
            for src_idx, _ in enumerate(self.source.rows):
                self.remove_highlighted_cell(self.m_source,src_idx+2, col_idx+1)
                self.m_source.add_highlighted_cell((src_idx + 2, col_idx+1), color=GREEN)
            self.scene.wait(0.3)
        self.set_up_target()
        # Move selected columns
        for tgt_col_idx, col_name in enumerate(cols):
            src_col_idx = self.source.labels.index(col_name)

            # Group all cells in the column (excluding header)
            source_col = VGroup(*[self.m_source.get_rows()[row_idx + 1][src_col_idx]
                for row_idx in range(self.source.num_rows)])

            target_col = VGroup(*[self.m_target.get_rows()[row_idx + 1][tgt_col_idx]
                for row_idx in range(self.target.num_rows)])

            # Animate the entire column transferring
            col_copy = source_col.copy().move_to(target_col)
            self.scene.play(TransformFromCopy(source_col, col_copy), run_time=1)

class DropAnimation(TableAnimation):
    def animate(self,cols):
        # Makes single column a list with one entry
        if isinstance(cols, str):
            cols = [cols]
        self.set_up_source()
        for col_name in cols:
            col_idx = self.source.labels.index(col_name)
            self.highlight_column_header(col_idx,RED)

            # Highlight column cells 
            for src_idx, _ in enumerate(self.source.rows):
                self.remove_highlighted_cell(self.m_source,src_idx+2, col_idx+1)
                self.m_source.add_highlighted_cell((src_idx + 2, col_idx+1), color=RED)
            self.scene.wait(0.3)
        self.set_up_target()
        # Move selected columns
        select_cols = [i for i in self.source.labels if i not in cols] # Drop difference
        for tgt_col_idx, col_name in enumerate(select_cols):
            src_col_idx = self.source.labels.index(col_name)

            # Group all cells in the column (excluding header)
            source_col = VGroup(*[self.m_source.get_rows()[row_idx + 1][src_col_idx]
                for row_idx in range(self.source.num_rows)])

            target_col = VGroup(*[self.m_target.get_rows()[row_idx + 1][tgt_col_idx]
                for row_idx in range(self.target.num_rows)])

            # Animate the entire column transferring
            col_copy = source_col.copy().move_to(target_col)
            self.scene.play(TransformFromCopy(source_col, col_copy), run_time=1)

class TakeAnimation(TableAnimation):
    def animate(self):
        # e.g. -> animate("Protein") -> animation for filtering where "Protein" column has specific value
        # Highlight column
        self.set_up_source()

        # Highlight row cells
        for src_idx in range(self.source.num_rows):
            if src_idx in self.match_map:
                for col_idx in range(len(self.source.labels)):
                    self.m_source.add_highlighted_cell((src_idx + 2, col_idx), color=GREEN)
                self.scene.wait(0.5)

        # Move matching rows
        self.set_up_target()
        for src_idx, tgt_idx in self.match_map.items():
            src_row = self.m_source.get_rows()[src_idx + 1]
            tgt_row = self.m_target.get_rows()[tgt_idx + 1]
            row_copy = src_row.copy()
            row_copy.move_to(tgt_row)
            self.scene.play(TransformFromCopy(src_row, row_copy))
            tgt_row.set_opacity(1)
            self.scene.wait()

class GroupAnimation(TableAnimation):
    def animate(self,col_name:str,collect='count'):
        # e.g. -> animate("Protein") -> animation for filtering where "Protein" column has specific value
        
        self.set_up_source()
        self.generate_text(col_name,collect)
        col_idx = self.source.labels.index(col_name)
        self.highlight_column_header(col_idx,RED)

        # Highlight column cells
        self.highlight_groups(col_name,collect) 

        self.set_up_target()

    def generate_text(self,col_name:str,collect='count'):
        if collect == 'count':
            text1 = Text(f'column(s) = "{col_name}",  collect_function = {collect}',color=BLACK)
            text2 = Text(f'For every unique value in "{col_name}", {collect} the number of rows',color=BLACK)

        text1.scale(0.5).shift(DOWN*2)
        text2.scale(0.5).shift(DOWN*2.5)
        self.scene.play(Write(text1))
        self.scene.play(Write(text2))

    def highlight_groups(self,col_name:str,collect='count'):
        col_idx = self.source.labels.index(col_name)
        # Get unique group keys from the first column of the target
        group_keys = [row[0] for row in self.target.rows]
        unique_keys = list(dict.fromkeys(group_keys))  # preserves order

        # Generate map from each group to unique color
        num_keys = len(unique_keys)
        colors = [interpolate_color(ORANGE, BLUE, alpha / max(1, num_keys - 1)) for alpha in range(num_keys)]
        group_color_map = dict(zip(unique_keys, colors))

        # For each group, highlight matching rows in source table
        for group_key in unique_keys:
            color = group_color_map[group_key]

            for src_idx, row in enumerate(self.source.rows):
                if row[col_idx] == group_key:
                    self.m_source.add_highlighted_cell((src_idx + 2, col_idx+1), color=color)
            self.scene.wait(1.5)    
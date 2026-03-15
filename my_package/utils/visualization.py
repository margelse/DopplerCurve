import matplotlib.pyplot as plt

class VisualizationPlots:
    def __init__(
            self,
            figsize:tuple,
            title_figure:str=None,
            grid_visible:bool=False
    ):
        self.figsize = figsize
        self.title = title_figure
        self.grid_visible = grid_visible
    
    def _add_parametres_plot(self, ax):
        ax.grid(visible=self.grid_visible)
        ax.set_title(self.title)
        ax.legend()

    def create_plot(self, x:list, y:list, labels:list):
        fig, ax = plt.subplots(figsize=self.figsize)

        for independent_var, line, name in zip(x, y, labels):
            ax.plot(independent_var, line, label=name)

        self._add_parametres_plot(ax)
        plt.show()
import pygame
import pydot

class Node():
    def __init__(self, node, font, font_color, background_color):
        self.node = node
        self.surface = self.draw_node(node, font, font_color, background_color)
        self.surface_selected = self.draw_node(node, font, background_color, font_color)

    def draw_node(self, node, font, font_color, background_color):
        surf = font.render(self.node.get("label"), True, font_color)
        new_surf = pygame.Surface((surf.get_width()+4, surf.get_height()+4))
        new_surf.fill(background_color)

        new_surf.fill(font_color, ((0,0,new_surf.get_width(),2)))
        new_surf.fill(font_color, ((0,new_surf.get_height()-2, new_surf.get_width(),new_surf.get_height())))
        new_surf.fill(font_color, ((0,0,2,new_surf.get_height())))
        new_surf.fill(font_color, ((new_surf.get_width()-2,0,new_surf.get_width(),new_surf.get_height())))
        
        new_surf.blit(surf, (2,2))
        return new_surf

class Visualizer():
    def __init__(self, graph):
        pygame.init()
        self.window = pygame.display.set_mode(size=(800,600))
        self.done = False
        self.graph = graph
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.font_color = pygame.Color(255,255,255)
        self.background_color = pygame.Color(0,0,0)
        self.nodes = [Node(node, self.font, self.font_color, self.background_color) for node in self.graph.get_nodes()]
        self.node_rects = []
        self.selected = None
    
    def draw_graph(self, root=None):
        self.node_rects = []
        if(root == None):
            draw_nodes = [node for node in self.nodes if "1" in node.node.get("class")]
        else:
            draw_nodes = [self.selected]
            edges = [edge.get_destination() for edge in self.graph.get_edges() if edge.get_source() == self.selected.node.get_name()]
            draw_nodes += [node for node in self.nodes if node.node.get_name() in edges]
            
        for (i,node) in enumerate(draw_nodes):
            if(self.selected == node):
                self.node_rects.append((self.window.blit(node.surface_selected, (10, i*20)), node))
            else:
                self.node_rects.append((self.window.blit(node.surface, (10, i*20)), node))
                
            

    def main_loop(self):
        while not self.done:
            self.window.fill(self.background_color)
            self.draw_graph(root = self.selected)
            pygame.display.flip()
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for node in self.node_rects:
                        if(node[0][0] < event.pos[0] < node[0][0]+node[0][2]):
                            if(node[0][1] < event.pos[1] < node[0][1]+node[0][3]):
                                if(self.selected == node[1]):
                                    self.selected = None
                                else:
                                    self.selected = node[1]

if __name__ == "__main__":
    graphs = pydot.graph_from_dot_file("1100.dot")
    nodes = graphs[0].get_nodes()
    for node in nodes:
        print(node.get("class"))
    lower = [node for node in nodes if "2" in node.get("class")]
    for node in lower:
        print(node)
        print(node.get("label"))
    v = Visualizer(graphs[0])
    v.main_loop()

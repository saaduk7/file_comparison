class Differences:
    """
    Interface for differneces that can be annotated.
    """
    def __init__(self, curve_color=False, layout=False, legend_values=False, x_axis_range=False, y_axis_range=False, missing_curves=False, shifted_pixels=False):
       
        self.curve_color = curve_color
        self.layout = layout
        self.legend_values = legend_values
        self.x_axis_range = x_axis_range
        self.y_axis_range = y_axis_range
        self.missing_curves = missing_curves
        self.shifted_pixels = shifted_pixels
    
class Position:
    def __init__(self, x, y, relative_position=None):
        self.x = x
        self.y = y
        self.relative_position = relative_position
    
    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.relative_position == other.relative_position
    
class Color:
    def __init__(self, line, background):
        self.line = line
        self.background = background
        
class Scaling:
    def __init__(self, auto_scaling_type, begin, end, origin, tick_distance, mini_tick_count):
        self.auto_scaling_type = auto_scaling_type
        self.begin = begin
        self.end = end 
        self.origin = origin 
        self.tick_distance = tick_distance
        self.mini_tick_count = mini_tick_count
        
    def __eq__(self, other): 
        if not isinstance(other, Scaling):
                return NotImplemented
        return self.auto_scaling_type == other.auto_scaling_type and self.begin == other.begin and self.end == other.end and self.origin == other.origin and self.tick_distance == other.tick_distance and self.mini_tick_count == other.mini_tick_count
        
class Curve:
    def __init__(self, name, shapetype, shape_x, shape_y, shape_line_color):
        self.name = name
        self.shapetype = shapetype
        self.shape_x = shape_x.split("_")[-1]
        self.shape_y = shape_y.split("_")[-1]
        self.shape_line_color = shape_line_color
    
    def __eq__(self, other): 
        if not isinstance(other, Curve):
                return NotImplemented
        diffence_list = list()
        if self.shapetype == other.shapetype and self.shape_x == other.shape_x and self.shape_y==other.shape_y:
            if self.shape_line_color != other.shape_line_color:
                diffence_list.append(f"Different Curve Color for Curve: {self.shape_y}")
            if diffence_list:
                return diffence_list
            else:
                return True
        else:
            return False
class Column:
    def __init__(self, alignment, bold_font, relative_column_width):
        self.alignment = alignment
        self.bold_font = bold_font
        self.relative_column_width = relative_column_width
    
    def __eq__(self, other): 
        if not isinstance(other, Column):
            return NotImplemented
        
        
class Cell:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        
    def __eq__(self, other): 
        if not isinstance(other, Cell):
            return NotImplemented
        if self.x == other.x and self.y == other.y:
            if self.text != other.text:
                return f"Different Legend Value at Cell({self.x},{self.y})"
            else:
                return True
        else:
            return False

class Frame:
    def __init__(self, filename, name, json_dict):
        self.filename = filename
        self.name = name
        self.position_1 = Position(json_dict["Position.X1"], json_dict["Position.Y1"])
        self.position_2 = Position(json_dict["Position.X2"], json_dict["Position.Y2"])
        self.color = Color(json_dict["Color.Line"], json_dict["Color.Background"])


class Image:
    def __init__(self, filename, name, json_dict):
        self.filename = filename
        self.name = name
        self.imagename = json_dict["FileName"]
        self.position_1 = Position(json_dict["Position.X1"], json_dict["Position.Y1"])
        self.position_2 = Position(json_dict["Position.X2"], json_dict["Position.Y2"])
        self.position_relative_position = json_dict["Position.RelativePosition"]

    def __eq__(self, other): 
        if not isinstance(other, Image):
            return NotImplemented
        if self.position_1 == other.position_1 and self.position_2 == other.position_2 and self.position_relative_position == other.position_relative_position:
            if self.imagename != other.imagename:
                return [f"Different image name {other.imagename} instead {self.imagename} of for Image {self.name}."]
            else:
                return True
        else:
            return False

class Comment:
    def __init__(self, filename, name, json_dict):
        self.filename = filename
        self.name = name
        self.text = json_dict["Text"]
        self.size = json_dict["Size"]
        self.color = json_dict["Color"]
        self.position_1 = Position(json_dict["Position.X1"], json_dict["Position.Y1"])
        self.position_2 = Position(json_dict["Position.X2"], json_dict["Position.Y2"])


    def __eq__(self, other): 
        if not isinstance(other, Comment):
            return NotImplemented
        if self.position_1 == other.position_1 and self.position_2 == other.position_2:
            if self.text != other.text:
                return [f"Different Text Values {other.text} instead {self.text} of for Comment {self.name}."]
            else:
                return True
        else:
            return False

class Text:
    def __init__(self, filename, name, json_dict):
        self.filename = filename
        self.name = name
        self.text = json_dict["Text"]
        self.size = json_dict["Size"]
        self.color = json_dict["Color"]
        self.position_1 = Position(json_dict["Position.X"], json_dict["Position.Y"])
        self.position_relative_position = json_dict["Position.RelativePosition"]

class TwoDAxisSystem:
    """
    2DAxisSystem class which is build up using other classes like 
    Position and Scaling.
    """
    def __init__(self, filename, name, json_dict):
        self.filename = filename
        self.name = name
        self.position_1 = Position(json_dict["Position.X1"], json_dict["Position.Y1"])
        self.position_2 = Position(json_dict["Position.X2"], json_dict["Position.Y2"])
        self.x_scaling = Scaling(json_dict["X.Scaling.AutoScalingType"], json_dict["X.Scaling.Begin"], 
                            json_dict["X.Scaling.End"], json_dict["X.Scaling.Origin"], 
                            json_dict["X.Scaling.Tick.Distance"], json_dict["X.Scaling.MiniTickCount"])
        self.y_scaling = Scaling(json_dict["Y1.Scaling.AutoScalingType"], json_dict["Y1.Scaling.Begin"], 
                            json_dict["Y1.Scaling.End"], json_dict["Y1.Scaling.Origin"], 
                            json_dict["Y1.Scaling.Tick.Distance"], json_dict["Y1.Scaling.MiniTickCount"])
        self.curve_dict = {}
        for key in json_dict:
            if key.startswith("Curve") and key.endswith(".Name"):
                curve_number = key.split(".")[0]
                if json_dict[curve_number+".ShapeType"] == 0:
                    temp_x = json_dict[curve_number+".Shape.XChannel"]
                    temp_y = json_dict[curve_number+".Shape.YChannel"]
                elif json_dict[curve_number+".ShapeType"] == 6:
                    temp_x = json_dict[curve_number+".Shape.XConstant"]
                    temp_y = json_dict[curve_number+".Shape.YConstant"]
                    
                self.curve_dict["curve_"+str(key[key.find("(")+1: key.find(")")])] = Curve(json_dict[key],
                           json_dict[curve_number+".ShapeType"], temp_x, temp_y, 
                             json_dict[curve_number+".Shape.Line.Color"])
        self.curve_count = json_dict["Curves.Count"]
    
    def __eq__(self, other):
        if not isinstance(other, TwoDAxisSystem):
            return NotImplemented
        difference_list = list()
        if self.name == other.name:
            if self.position_1 != other.position_1:
                difference_list.append(f"Shifted Position 1 for 2DAxisSystem: {self.name}")
            if self.position_2 != other.position_2:
                difference_list.append(f"Shifted Position 2 for 2DAxisSystem: {self.name}")
            if self.x_scaling != other.x_scaling:
                difference_list.append(f"Different X_Scaling for 2DAxisSystem: {self.name}")
            if self.y_scaling != other.y_scaling:
                difference_list.append(f"Different Y_Scaling for 2DAxisSystem: {self.name}")

            curve_diff = self.curve_count - other.curve_count
            
            if curve_diff != 0:
                if curve_diff < 0:
                    difference_list.append(f"Missing Curve in {self.filename}")
                else:
                    difference_list.append(f"Missing Curve in {other.filename}")

            for curve_key, curve_value in self.curve_dict.items():
                for other_key, other_value in other.curve_dict.items():
                    cmp = curve_value == other_value
                    if type(cmp) is list:
                        difference_list.extend(cmp)
                    elif cmp == True:
                        break
            if difference_list:
                return difference_list
            else:
                return True
        else:
            return False

class TwoDTable:
    """
    2DTable class which is build up using other classes like Position,
    Column, Cell etc
    """
    def __init__(self, filename, name, json_dict):
        self.filename = filename
        self.name = name
        self.position_1 = Position(json_dict["Position.X1"], json_dict["Position.Y1"])
        self.position_2 = Position(json_dict["Position.X2"], json_dict["Position.Y2"])
        self.settings_border_line_color = json_dict["Settings.BorderLineColor"]
        
        self.column_dict = {}
        self.cell_list = list()
        for key in json_dict:
            if key.startswith("Column") and key.endswith(".RelativeColumnWidth"):
                column_number = key.split(".")[0]
                self.column_dict["column_"+str(key[key.find("(")+1: key.find(")")])] = Column(json_dict[column_number+".Settings.RelativeColumnWidth"],
                                                    json_dict[column_number+".Settings.Alignment"],
                                                    json_dict[column_number+".Settings.Font.Bold"])
            elif key.startswith("Cell"):
                cell_coords = key[key.find("(")+1: key.find(")")]
                self.cell_list.append(Cell(cell_coords.split(",")[0], cell_coords.split(",")[-1], json_dict[key]))
    
    def __eq__(self, other): 
        if not isinstance(other, TwoDTable):
            return NotImplemented
        difference_list = list()
        if self.position_1 == other.position_1 and self.position_2 == other.position_2 and len(self.column_dict) == len(other.column_dict):
            for cell in self.cell_list:
                for other_cell in other.cell_list:
                    cmp = cell == other_cell
                    if type(cmp) is str:
                        difference_list.append(cmp)
                    elif cmp is True:
                        break
            if difference_list:
                return difference_list
            else:
                return True
        else:
            return False        
        

class JsonReport:
    """ 
    Creates a json report which is the reperesentation of json file.
    Provides functionality to compare with another json report.
    """
    def __init__(self, filename, json_dict):
        self.filename = filename
        self.objects_dict = {}
        for key, item in json_dict.items():
            if item["Type"] == "2DAxisSystem":
                if "2DAxisSystem" not in self.objects_dict:
                    self.objects_dict["2DAxisSystem"] = list()
                self.objects_dict["2DAxisSystem"].append(TwoDAxisSystem(filename, key, item))
            elif item["Type"] == "2DTable":
                if "2DTable" not in self.objects_dict:
                    self.objects_dict["2DTable"] = list()
                self.objects_dict["2DTable"].append(TwoDTable(filename, key, item))
            else:
                if item["Type"] not in self.objects_dict:
                    self.objects_dict[item["Type"]] = list()
                self.objects_dict[item["Type"]].append(globals()[item["Type"]](filename, key, item))
                
    @staticmethod
    def two_d_table_comparison(sys_1, sys_2):
        difference_list = list()
        if len(sys_1) != len(sys_2):
            difference_list.append("Different Number of Tables")
        for table in sys_1:
            for other_table in sys_2:
                cmp = table == other_table
                if type(cmp) is list:
                    #difference_list.append(f"{table.filename}: {table.name}: {cmp}")
                    difference_list.append(f"{table.name}: {cmp}")
                elif cmp is True:
                    break
        if difference_list:
                return difference_list
        else:
            return True
    
    @staticmethod
    def text_comparison(sys_1, sys_2):
        difference_list = list()
        if len(sys_1) != len(sys_2):
            difference_list.append("Different Number of Text Fields")
        for text in sys_1:
            for other_text in sys_2:
                cmp = text == other_text
                if type(cmp) is list:
                    difference_list.append(f"{table.filename}: {table.name}: {cmp}")
                elif cmp is True:
                    break
        if difference_list:
                return difference_list
        else:
            return True
        
    
    def __eq__(self, other): 
        if not isinstance(other, JsonReport):
            return NotImplemented
        tmp_list = list()
        
        for cls_list in self.objects_dict:
            if cls_list == "2DTable":
                tmp_list.append(JsonReport.two_d_table_comparison(self.objects_dict[cls_list], other.objects_dict[cls_list]))
            elif cls_list == "Text":
                tmp_list.append(JsonReport.text_comparison(self.objects_dict[cls_list], other.objects_dict[cls_list]))
            else:
                for idx, item in enumerate(self.objects_dict[cls_list]):
                    tmp_list.append(item == other.objects_dict[cls_list][idx])
        
        # difference_list = [val for val in difference_list if isinstance(val, list)] 
        difference_list = list()
        for val in tmp_list:
            if isinstance(val, bool):
                pass
            else:
                difference_list += (val)
        
        return difference_list

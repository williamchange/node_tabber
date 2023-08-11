import bpy
import itertools

DATA_TYPE = ["FLOAT", "INT", "FLOAT_VECTOR", "FLOAT_COLOR", "BOOLEAN"]
DOMAIN = ["POINT", "EDGE", "FACE", "CORNER", "SPLINE", "INSTANCE"]
MAPPING = ["INTERPOLATED", "NEAREST"]
COMPONENT = ["MESH", "POINTCLOUD", "CURVE", "INSTANCES"]
SPLINE_TYPE = ["CATMULL_ROM", "POLY", "BEZIER", "NURBS"]
TARGET_EL = ["POINTS", "EDGES", "FACES"]
INTERPOLATION = ["LINEAR", "STEPPED", "SMOOTHSTEP", "SMOOTHERSTEP"]
OPERATION = ["INTERSECT", "UNION", "DIFFERENCE"]
SCALE_EL_MODES = ["UNIFORM", "SINGLE_AXIS"]
ROUNDING_MODES = ["FLOOR", "CEILING", "ROUND", "TRUNCATE"]

GN_CMP_VEC_MODES = ["ELEMENT", "LENGTH", "DOT_PRODUCT", "AVERAGE", "DIRECTION"]
GN_CMP_OPS = [
    "LESS_THAN",
    "LESS_EQUAL",
    "GREATER_THAN",
    "GREATER_EQUAL",
    "EQUAL",
    "NOT_EQUAL",
    "BRIGHTER",
    "DARKER",
]

FILTER_MODES = [
    "SOFTEN",
    "BOX",
    "DIAMOND",
    "LAPLACE",
    "SOBEL",
    "PREWITT",
    "KIRSCH",
    "SHADOW",
]


def replace_dtype_labels(string):
    return string.replace("FLOAT_", "").replace("INT", "integer").replace("_", " ")


def gen_subnodes(a, b, setting1, setting2):
    output = [
        [
            f'{a} {d0} {d1}',
            f'{b}  ▸  {str.title(replace_dtype_labels(d0))} {str.title(d1).replace("_", "")} ({d0.replace("FLOAT_", "")[0]}{d1[0]})'
        ]
        for d0, d1 in itertools.product(setting1, setting2)]
    return output


def gen_dtype_subnodes(a, b):
    output = [
        [
            f'{a} {d}',
            f'{b}  ▸  {str.title(replace_dtype_labels(d))} ({str.title(replace_dtype_labels(d)[0])})'
        ]
        for d in DATA_TYPE
    ]
    return output


def gen_non_dtype_subnodes(a, b, setting1):
    output = [
        [
            f'{a} {d}',
            f'{b}  ▸  {str.title(d).replace("_", " ").replace("Pointcloud", "Point Cloud")} ({d[0]})',
        ]
        for d in setting1
    ]
    return output


def gn_cmp_str_col(a, setting1, setting2):
    return [
        [
            f'CMP {a} {d1}',
            f'Compare  ▸  {str.title(d0)}  ▸  {str.title(d1.replace("_", " "))} (C{d0[0] + d1[0]})'
        ]
        for d0, d1 in itertools.product(setting1, setting2)
    ]


def op_abbr(s):
    return "".join([c[0] for c in s.split("_")])


gn_cmp_str = gn_cmp_str_col("STRING", ["STRING"], GN_CMP_OPS[4:-2])
gn_cmp_col = gn_cmp_str_col("RGBA", ["COLOR"], GN_CMP_OPS[4:])

gn_cmp_fl_it = [
    [
        f'CMP {d0} {d1}',
        f'Compare  ▸  {str.title(replace_dtype_labels((d0)))}  ▸  {str.title(d1).replace("_", " ")} (C{d0[0] + op_abbr(d1)})'
    ]
    for d0, d1 in itertools.product(["FLOAT", "INT"], GN_CMP_OPS[:-2])
]

gn_cmp_vec = [
    [
        f'CMP VECTOR {d0} {d1}',
        f'Compare  ▸  Vector  ▸  {str.title(d0).replace("_", " ").replace(" Product", "")} {str.title(d1).replace("_", " ")} (CV{d0[0] + op_abbr(d1)})'
    ]
    for d0, d1 in itertools.product(GN_CMP_VEC_MODES, GN_CMP_OPS[:-2])
]


c_filter = [
    [
        f'F {ft.replace("DIAMOND", "SHARPEN_DIAMOND").replace("BOX","SHARPEN")}',
        f'Filter  ▸  {str.title(ft.replace("DIAMOND", "Diamond Sharpen").replace("BOX", "Box Sharpen"))} ({ft[0]})'
    ]
    for ft in FILTER_MODES
]

math = [
    [" M ADD", "Math  ▸  Add (A)"],
    [" M SUBTRACT", "Math  ▸  Subtract (S)"],
    [" M MULTIPLY", "Math  ▸  Multiply (M)"],
    [" M DIVIDE", "Math  ▸  Divide (D)"],
    [" M MULTIPLY_ADD", "Math  ▸  Multiply Add (MA)"],
    [" M POWER", "Math  ▸  Power (P)"],
    [" M LOGARITHM", "Math  ▸  Logarithm (L)"],
    [" M SQRT", "Math  ▸  Square Root (SQ)"],
    [" M INVERSE_SQRT", "Math  ▸  Inverse Square Root (ISQ)"],
    [" M ABSOLUTE", "Math  ▸  Absolute (A)"],
    [" M EXPONENT", "Math  ▸  Exponent (E)"],
    [" M MINIMUM", "Math  ▸  Minimum (M)"],
    [" M MAXIMUM", "Math  ▸  Maximum (M)"],
    [" M LESS_THAN", "Math  ▸  Less Than (LT)"],
    [" M GREATER_THAN", "Math  ▸  Greater Than (GT)"],
    [" M SIGN", "Math  ▸  Sign (S)"],
    [" M COMPARE", "Math  ▸  Compare (C)"],
    [" M SMOOTH_MIN", "Math  ▸  Smooth Minimum (SM)"],
    [" M SMOOTH_MAX", "Math  ▸  Smooth Maximum (SM)"],
    [" M ROUND", "Math  ▸  Round (R)"],
    [" M FLOOR", "Math  ▸  Floor (F)"],
    [" M CEIL", "Math  ▸  Ceiling (C)"],
    [" M TRUNC", "Math  ▸  Truncate (T)"],
    [" M FRACT", "Math  ▸  Fraction (F)"],
    [" M MODULO", "Math  ▸  Modulo (M)"],
    [" M WRAP", "Math  ▸  Wrap (W)"],
    [" M SNAP", "Math  ▸  Snap (S)"],
    [" M PINGPONG", "Math  ▸  Ping-Pong (PP)"],
    [" M SINE", "Math  ▸  Sine (S)"],
    [" M COSINE", "Math  ▸  Cosine (C)"],
    [" M TANGENT", "Math  ▸  Tangent (T)"],
    [" M ARCSINE", "Math  ▸  Arcsine (AS)"],
    [" M ARCCOSINE", "Math  ▸  Arccosine (AC)"],
    [" M ARCTANGENT", "Math  ▸  Arctangent (AT)"],
    [" M ARCTAN2", "Math  ▸  Arctan2 (AT)"],
    [" M SINH", "Math  ▸  Hyperbolic Sine (HS)"],
    [" M COSH", "Math  ▸  Hyperbolic Cosine (HC)"],
    [" M TANH", "Math  ▸  Hyperbolic Tangent (HT)"],
    [" M RADIANS", "Math  ▸  To Radians (TR)"],
    [" M DEGREES", "Math  ▸  To Degrees (TD)"],
]

math_symb = [
    [" M ADD", "Math  ▸  Add (+)"],
    [" M SUBTRACT", "Math  ▸  Subtract (-)"],
    [" M MULTIPLY", "Math  ▸  Multiply (*)"],
    [" M DIVIDE", "Math  ▸  Divide (/)"],
    [" M MULTIPLY_ADD", "Math  ▸  Multiply Add (*+)"],
    [" M POWER", "Math  ▸  Power (^)"],
    [" M LOGARITHM", "Math  ▸  Logarithm (L)"],
    [" M SQRT", "Math  ▸  Square Root (SQ)"],
    [" M INVERSE_SQRT", "Math  ▸  Inverse Square Root (ISQ)"],
    [" M ABSOLUTE", "Math  ▸  Absolute (A)"],
    [" M EXPONENT", "Math  ▸  Exponent (E)"],
    [" M MINIMUM", "Math  ▸  Minimum (M)"],
    [" M MAXIMUM", "Math  ▸  Maximum (M)"],
    [" M LESS_THAN", "Math  ▸  Less Than (<)"],
    [" M GREATER_THAN", "Math  ▸  Greater Than (>)"],
    [" M SIGN", "Math  ▸  Sign (S)"],
    [" M COMPARE", "Math  ▸  Compare (C)"],
    [" M SMOOTH_MIN", "Math  ▸  Smooth Minimum (SM)"],
    [" M SMOOTH_MAX", "Math  ▸  Smooth Maximum (SM)"],
    [" M ROUND", "Math  ▸  Round (R)"],
    [" M FLOOR", "Math  ▸  Floor (F)"],
    [" M CEIL", "Math  ▸  Ceiling (C)"],
    [" M TRUNC", "Math  ▸  Truncate (T)"],
    [" M FRACT", "Math  ▸  Fraction (F)"],
    [" M MODULO", "Math  ▸  Modulo (M)"],
    [" M WRAP", "Math  ▸  Wrap (W)"],
    [" M SNAP", "Math  ▸  Snap (S)"],
    [" M PINGPONG", "Math  ▸  Ping-Pong (PP)"],
    [" M SINE", "Math  ▸  Sine (S)"],
    [" M COSINE", "Math  ▸  Cosine (C)"],
    [" M TANGENT", "Math  ▸  Tangent (T)"],
    [" M ARCSINE", "Math  ▸  Arcsine (AS)"],
    [" M ARCCOSINE", "Math  ▸  Arccosine (AC)"],
    [" M ARCTANGENT", "Math  ▸  Arctangent (AT)"],
    [" M ARCTAN2", "Math  ▸  Arctan2 (AT)"],
    [" M SINH", "Math  ▸  Hyperbolic Sine (HS)"],
    [" M COSH", "Math  ▸  Hyperbolic Cosine (HC)"],
    [" M TANH", "Math  ▸  Hyperbolic Tangent (HT)"],
    [" M RADIANS", "Math  ▸  To Radians (TR)"],
    [" M DEGREES", "Math  ▸  To Degrees (TD)"],
]

vec_math = [
    [" VM ADD", "Vector Math  ▸  Add (A)"],
    [" VM SUBTRACT", "Vector Math  ▸  Subtract (S)"],
    [" VM MULTIPLY", "Vector Math  ▸  Multiply (M)"],
    [" VM DIVIDE", "Vector Math  ▸  Divide (D)"],
    [" VM CROSS_PRODUCT", "Vector Math  ▸  Cross Product (CP)"],
    [" VM PROJECT", "Vector Math  ▸  Project (P)"],
    [" VM REFRACT", "Vector Math  ▸  Refract (R)"],
    [" VM REFLECT", "Vector Math  ▸  Reflect (R)"],
    [" VM DOT_PRODUCT", "Vector Math  ▸  Dot Product (DP)"],
    [" VM DISTANCE", "Vector Math  ▸  Distance (D)"],
    [" VM MULTIPLY_ADD", "Vector Math  ▸  Multiply Add (MA)"],
    [" VM FACEFORWARD", "Vector Math  ▸  Faceforward (F)"],
    [" VM LENGTH", "Vector Math  ▸  Length (L)"],
    [" VM SCALE", "Vector Math  ▸  Scale (S)"],
    [" VM NORMALIZE", "Vector Math  ▸  Normalize (N)"],
    [" VM ABSOLUTE", "Vector Math  ▸  Absolute (A)"],
    [" VM MINIMUM", "Vector Math  ▸  Minimum (M)"],
    [" VM MAXIMUM", "Vector Math  ▸  Maximum (M)"],
    [" VM FLOOR", "Vector Math  ▸  Floor (F)"],
    [" VM CEIL", "Vector Math  ▸  Ceiling (C)"],
    [" VM FRACTION", "Vector Math  ▸  Fraction (F)"],
    [" VM MODULO", "Vector Math  ▸  Modulo (M)"],
    [" VM WRAP", "Vector Math  ▸  Wrap (W)"],
    [" VM SNAP", "Vector Math  ▸  Snap (S)"],
    [" VM SINE", "Vector Math  ▸  Sine (S)"],
    [" VM COSINE", "Vector Math  ▸  Cosine (C)"],
    [" VM TANGENT", "Vector Math  ▸  Tangent (T)"],
]

vec_symb = [
    [" VM ADD", "Vector Math  ▸  Add (+)"],
    [" VM SUBTRACT", "Vector Math  ▸  Subtract (-)"],
    [" VM MULTIPLY", "Vector Math  ▸  Multiply (*)"],
    [" VM DIVIDE", "Vector Math  ▸  Divide (/)"],
    [" VM CROSS_PRODUCT", "Vector Math  ▸  Cross Product (x)"],
    [" VM PROJECT", "Vector Math  ▸  Project (P)"],
    [" VM REFRACT", "Vector Math  ▸  Refract (R)"],
    [" VM REFLECT", "Vector Math  ▸  Reflect (R)"],
    [" VM DOT_PRODUCT", "Vector Math  ▸  Dot Product (DP)"],
    [" VM DISTANCE", "Vector Math  ▸  Distance (D)"],
    [" VM MULTIPLY_ADD", "Vector Math  ▸  Multiply Add (*+)"],
    [" VM FACEFORWARD", "Vector Math  ▸  Faceforward (F)"],
    [" VM LENGTH", "Vector Math  ▸  Length (L)"],
    [" VM SCALE", "Vector Math  ▸  Scale (*)"],
    [" VM NORMALIZE", "Vector Math  ▸  Normalize (N)"],
    [" VM ABSOLUTE", "Vector Math  ▸  Absolute (A)"],
    [" VM MINIMUM", "Vector Math  ▸  Minimum (M)"],
    [" VM MAXIMUM", "Vector Math  ▸  Maximum (M)"],
    [" VM FLOOR", "Vector Math  ▸  Floor (F)"],
    [" VM CEIL", "Vector Math  ▸  Ceiling (C)"],
    [" VM FRACTION", "Vector Math  ▸  Fraction (F)"],
    [" VM MODULO", "Vector Math  ▸  Modulo (M)"],
    [" VM WRAP", "Vector Math  ▸  Wrap (W)"],
    [" VM SNAP", "Vector Math  ▸  Snap (S)"],
    [" VM SINE", "Vector Math  ▸  Sine (S)"],
    [" VM COSINE", "Vector Math  ▸  Cosine (C)"],
    [" VM TANGENT", "Vector Math  ▸  Tangent (T)"],
]

color = [
    [" C VALUE", "Mix Color  ▸  Value (V)"],
    [" C COLOR", "Mix Color  ▸  Color (C)"],
    [" C SATURATION", "Mix Color  ▸  Saturation (S)"],
    [" C HUE", "Mix Color  ▸  Hue (H)"],
    [" C DIVIDE", "Mix Color  ▸  Divide (D)"],
    [" C SUBTRACT", "Mix Color  ▸  Subtract (S)"],
    [" C DIFFERENCE", "Mix Color  ▸  Difference (D)"],
    [" C LINEAR_LIGHT", "Mix Color  ▸  Linear Light (LL)"],
    [" C SOFT_LIGHT", "Mix Color  ▸  Soft Light (SL)"],
    [" C OVERLAY", "Mix Color  ▸  Overlay (O)"],
    [" C ADD", "Mix Color  ▸  Add (A)"],
    [" C DODGE", "Mix Color  ▸  Dodge (D)"],
    [" C SCREEN", "Mix Color  ▸  Screen (S)"],
    [" C LIGHTEN", "Mix Color  ▸  Lighten (L)"],
    [" C BURN", "Mix Color  ▸  Burn (B)"],
    [" C MULTIPLY", "Mix Color  ▸  Multiply (M)"],
    [" C DARKEN", "Mix Color  ▸  Darken (D)"],
    [" C MIX", "Mix Color  ▸  Mix (M)"],
]

bool_math = [
    [" BM AND", "Boolean Math  ▸  And (A)"],
    [" BM OR", "Boolean Math  ▸  Or (O)"],
    [" BM NOT", "Boolean Math  ▸  Not (N)"],
    [" BM NAND", "Boolean Math  ▸  Not And (NA)"],
    [" BM NOR", "Boolean Math  ▸  Nor (N)"],
    [" BM XNOR", "Boolean Math  ▸  Equal (E)"],
    [" BM XOR", "Boolean Math  ▸  Not Equal (NE)"],
    [" BM IMPLY", "Boolean Math  ▸  Imply (I)"],
    [" BM NIMPLY", "Boolean Math  ▸  Subtract (S)"],
]

bool_symb = [
    [" BM AND", "Boolean Math  ▸  And (^)"],
    [" BM OR", "Boolean Math  ▸  Or (v)"],
    [" BM NOT", "Boolean Math  ▸  Not (~)"],
    [" BM NAND", "Boolean Math  ▸  Not And (~^)"],
    [" BM NOR", "Boolean Math  ▸  Nor (~v)"],
    [" BM XNOR", "Boolean Math  ▸  Equal (=)"],
    [" BM XOR", "Boolean Math  ▸  Not Equal (~=)"],
    [" BM IMPLY", "Boolean Math  ▸  Imply (->)"],
    [" BM NIMPLY", "Boolean Math  ▸  Subtract (-)"],
]

rand_val = [
    [" RV FLOAT", "Random Value  ▸  Float (F)"],
    [" RV INT", "Random Value  ▸  Integer (I)"],
    [" RV FLOAT_VECTOR", "Random Value  ▸  Vector (V)"],
    [" RV BOOLEAN", "Random Value  ▸  Boolean (B)"],
]

switch = [
    [" SW FLOAT", "Switch  ▸  Float (F)"],
    [" SW INT", "Switch  ▸  Integer (I)"],
    [" SW BOOLEAN", "Switch  ▸  Boolean (B)"],
    [" SW VECTOR", "Switch  ▸  Vector (V)"],
    [" SW STRING", "Switch  ▸  String (S)"],
    [" SW RGBA", "Switch  ▸  Color (C)"],
    [" SW OBJECT", "Switch  ▸  Object (O)"],
    [" SW IMAGE", "Switch  ▸  Image (I)"],
    [" SW GEOMETRY", "Switch  ▸  Geometry (G)"],
    [" SW COLLECTION", "Switch  ▸  Collection (C)"],
    [" SW TEXTURE", "Switch  ▸  Texture (T)"],
    [" SW MATERIAL", "Switch  ▸  Material (M)"],
]

sep_col = [
    [" SEP RGB", "Separate Color  ▸  RGB (SR)"],
    [" SEP HSV", "Separate Color  ▸  HSV (SH)"],
    [" SEP HSL", "Separate Color  ▸  HSL (SL)"],
]

com_col = [
    [" COM RGB", "Combine Color  ▸  RGB (CR)"],
    [" COM HSV", "Combine Color  ▸  HSV (CH)"],
    [" COM HSL", "Combine Color  ▸  HSL (CL)"],
]

vec_rot = [
    [" VR AXIS_ANGLE", "Vector Rotate  ▸  Axis Angle (VRA)"],
    [" VR X_AXIS", "Vector Rotate  ▸  X Axis (VRX)"],
    [" VR Y_AXIS", "Vector Rotate  ▸  Y Axis (VRY)"],
    [" VR Z_AXIS", "Vector Rotate  ▸  Z Axis (VRZ)"],
    [" VR EULER_XYZ", "Vector Rotate  ▸  Euler (VRE)"],
]

uv_unwrap = [
    [" UU ANGLE_BASED", "UV Unwrap  ▸  Angle Based (AB)"],
    [" UU CONFORMAL", "UV Unwrap  ▸  Conformal (C)"],
]

fillet_curve = [
    [" FC BEZIER", "Fillet Curve  ▸  Bezier (B)"],
    [" FC POLY", "Fillet Curve  ▸  Poly (P)"]
]

mix_nodes = [
    [" Mix Vector", "Mix Vector (MV)"]
]


dom_size = gen_non_dtype_subnodes("DS", "Domain Size", COMPONENT)
geo_prox = gen_non_dtype_subnodes("GPX", "Geometry Proximity", TARGET_EL)
sample_nearest = gen_non_dtype_subnodes("SN", "Sample Nearest", DOMAIN[:4])
set_spline_type = gen_non_dtype_subnodes("SPT", "Set Spline Type", SPLINE_TYPE)
merge_by_dist = gen_non_dtype_subnodes("MbD", "Merge by Distance", ["ALL", "CONNECTED"])
mesh_boolean = gen_non_dtype_subnodes("MB", "Mesh Boolean", OPERATION)
sep_geo = gen_non_dtype_subnodes("SG", "Separate Geometry", DOMAIN[:3] + DOMAIN[-2:])
dupe_el = gen_non_dtype_subnodes("DE", "Duplicate Elements", DOMAIN[:3] + DOMAIN[-2:])
float_to_int = gen_non_dtype_subnodes("FtI", "Float to Integer", ROUNDING_MODES)
blur_attr = gen_non_dtype_subnodes("BA", "Blur Attribute", ["FLOAT", "INT", "VECTOR", "COLOR"])

named_attr = gen_dtype_subnodes("NA", "Named Attribute")
sample_uv_surf = gen_dtype_subnodes("SUS", "Sample UV Surface")
sample_nearest_surf = gen_dtype_subnodes("SNS", "Sample Nearest Surface")

attr_stat = gen_subnodes("AST", "Attribute Statistic", ["FLOAT", "FLOAT_VECTOR"], DOMAIN)
raycast = gen_subnodes("RAY", "Raycast", DATA_TYPE, MAPPING)
store_named_attr = gen_subnodes("SNA", "Store Named Attribute", DATA_TYPE + ["2D_VECTOR"], DOMAIN)
capture_attr = gen_subnodes("CAP", "Capture Attribute", DATA_TYPE, DOMAIN)
evaluate_on_dom = gen_subnodes("INTER", "Evaluate on Domain", DATA_TYPE, DOMAIN)
sample_index = gen_subnodes("SIN", "Sample Index", DATA_TYPE, DOMAIN)
map_range = gen_subnodes("MR", "Map Range", ["FLOAT", "FLOAT_VECTOR"], INTERPOLATION)
evaluate_at_index = gen_subnodes("FaI", "Evaluate at Index", DATA_TYPE, DOMAIN)
scale_el = gen_subnodes("SE", "Scale Elements", DOMAIN[1:-3], SCALE_EL_MODES)
accum_field = gen_subnodes("AF", "Accumulate Field", ["FLOAT", "INT", "FLOAT_VECTOR"], DOMAIN)

def subnode_entries(use_symbols, editor_type):
    SUBNODE_ENTRIES = {
        "Math": math_symb if use_symbols else math,
        "Vector Math": vec_symb if use_symbols else vec_math,
        "Mix": mix_nodes + color if (editor_type == "GeometryNodeTree") else color,
        "Boolean Math": bool_symb if use_symbols else bool_math,
        "Random Value": rand_val,
        "Switch": switch,
        "Separate Color": sep_col,
        "Combine Color": com_col,
        "Domain Size": dom_size,
        "Geometry Proximity": geo_prox,
        "Sample Nearest": sample_nearest,
        "Sample Nearest Surface": sample_nearest_surf,
        "Sample UV Surface": sample_uv_surf,
        "Attribute Statistic": attr_stat,
        "Blur Attribute": blur_attr,
        "Raycast": raycast,
        "Store Named Attribute": store_named_attr,
        "Capture Attribute": capture_attr,
        "Evaluate on Domain": evaluate_on_dom,
        "Sample Index": sample_index,
        "Map Range": map_range if (editor_type != "CompositorNodeTree") else None,
        "Set Spline Type": set_spline_type,
        "Mesh Boolean": mesh_boolean,
        "Merge by Distance": merge_by_dist,
        "Separate Geometry": sep_geo,
        "Duplicate Elements": dupe_el,
        "Evaluate at Index": evaluate_at_index,
        "Scale Elements": scale_el,
        "Named Attribute": named_attr,
        "Vector Rotate": vec_rot,
        "Compare": gn_cmp_vec + gn_cmp_fl_it + gn_cmp_col + gn_cmp_str,
        "UV Unwrap": uv_unwrap,
        "Filter": c_filter,
        "Float to Integer": float_to_int,
        "Accumulate Field": accum_field,
        "Fillet Curve": fillet_curve
    }

    return SUBNODE_ENTRIES

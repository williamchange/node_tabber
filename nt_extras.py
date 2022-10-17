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
    return string.replace("FLOAT_", "").replace("INT", "integer")


def gen_subnodes(a, b, setting1, setting2):
    return [
        [
            " {} {} {}".format(a, d[0], d[1]),
            "{} {} ({}{}) {}".format(
                str.title(replace_dtype_labels(d[0])),
                str.title(d[1]).replace("_", ""),
                d[0].replace("FLOAT_", "")[0],
                d[1][0],
                b,
            ),
        ]
        for d in itertools.product(setting1, setting2)
    ]


def gen_dtype_subnodes(a, b):
    return [
        [
            " {} {}".format(a, d),
            "{} ({}) {}".format(
                str.title(replace_dtype_labels(d)),
                d[0],
                b,
            ),
        ]
        for d in DATA_TYPE
    ]


def gen_non_dtype_subnodes(a, b, setting1):
    return [
        [
            " {} {}".format(a, d),
            "{} ({}) {}".format(str.title(d).replace("_", " "), d[0], b),
        ]
        for d in setting1
    ]


def gn_cmp_str_col(a, setting1, setting2):
    return [
        [
            f" CMP {a} {d[1]}",
            "{} {} (C{}) COMP".format(
                str.title(d[0]),
                str.title(d[1].replace("_", " ")),
                d[0][0] + d[1][0],
            ),
        ]
        for d in itertools.product(setting1, setting2)
    ]


def op_abbr(s):
    return "".join([c[0] for c in s.split("_")])


gn_cmp_str = gn_cmp_str_col("STRING", ["STRING"], GN_CMP_OPS[4:-2])
gn_cmp_col = gn_cmp_str_col("RGBA", ["COLOR"], GN_CMP_OPS[4:])

gn_cmp_fl_it = [
    [
        f" CMP {d[0]} {d[1]}",
        "{} {} (C{}{}) COMP".format(
            str.title(replace_dtype_labels((d[0]))),
            str.title(d[1]).replace("_", " "),
            d[0][0],
            op_abbr(d[1]),
        ),
    ]
    for d in itertools.product(["FLOAT", "INT"], GN_CMP_OPS[:-2])
]

gn_cmp_vec = [
    [
        f" CMP VECTOR {d[0]} {d[1]}",
        "V {} {} (CV{}{}) COMP".format(
            str.title(d[0]).replace("_", " ").replace(" Product", ""),
            str.title(d[1]).replace("_", " "),
            d[0][0],
            op_abbr(d[1]),
        ),
    ]
    for d in itertools.product(GN_CMP_VEC_MODES, GN_CMP_OPS[:-2])
]

c_filter = [
    [
        f" F {ft.replace('DIAMOND', 'SHARPEN_DIAMOND').replace('BOX','SHARPEN')}",
        "{} ({}) FILTER".format(
            str.title(
                ft.replace("DIAMOND", "Diamond Sharpen").replace("BOX", "Box Sharpen")
            ),
            ft[0],
        ),
    ]
    for ft in FILTER_MODES
]

math = [
    [" M ADD", "Add (A) MATH"],
    [" M SUBTRACT", "Subtract (S) MATH"],
    [" M MULTIPLY", "Multiply (M) MATH"],
    [" M DIVIDE", "Divide (D) MATH"],
    [" M MULTIPLY_ADD", "Multiply Add (MA) MATH"],
    [" M POWER", "Power (P) MATH"],
    [" M LOGARITHM", "Logarithm (L) MATH"],
    [" M SQRT", "Square Root (SQ) MATH"],
    [" M INVERSE_SQRT", "Inverse Square Root (ISQ) MATH"],
    [" M ABSOLUTE", "Absolute (A) MATH"],
    [" M EXPONENT", "Exponent (E) MATH"],
    [" M MINIMUM", "Minimum (M) MATH"],
    [" M MAXIMUM", "Maximum (M) MATH"],
    [" M LESS_THAN", "Less Than (LT) MATH"],
    [" M GREATER_THAN", "Greater Than (GT) MATH"],
    [" M SIGN", "Sign (S) MATH"],
    [" M COMPARE", "Compare (C) MATH"],
    [" M SMOOTH_MIN", "Smooth Minimum (SM) MATH"],
    [" M SMOOTH_MAX", "Smooth Maximum (SM) MATH"],
    [" M ROUND", "Round (R) MATH"],
    [" M FLOOR", "Floor (F) MATH"],
    [" M CEIL", "Ceiling (C) MATH"],
    [" M TRUNC", "Truncate (T) MATH"],
    [" M FRACT", "Fraction (F) MATH"],
    [" M MODULO", "Modulo (M) MATH"],
    [" M WRAP", "Wrap (W) MATH"],
    [" M SNAP", "Snap (S) MATH"],
    [" M PINGPONG", "Ping-Pong (PP) MATH"],
    [" M SINE", "Sine (S) MATH"],
    [" M COSINE", "Cosine (C) MATH"],
    [" M TANGENT", "Tangent (T) MATH"],
    [" M ARCSINE", "ArcSine (AS) MATH"],
    [" M ARCCOSINE", "Arccosine (AC) MATH"],
    [" M ARCTANGENT", "Arctangent (AT) MATH"],
    [" M ARCTAN2", "Arctan2 (AT) MATH"],
    [" M SINH", "Hyperbolic Sine (HS) MATH"],
    [" M COSH", "Hyperbolic Cosine (HC) MATH"],
    [" M TANH", "Hyperbolic Tangent (HT) MATH"],
    [" M RADIANS", "To Radians (TR) MATH"],
    [" M DEGREES", "To Degrees (TD) MATH"],
]

vec_math = [
    [" VM ADD", "Add (A) VEC MATH"],
    [" VM SUBTRACT", "Subtract (S) VEC MATH"],
    [" VM MULTIPLY", "Multiply (M) VEC MATH"],
    [" VM DIVIDE", "Divide (D) VEC MATH"],
    [" VM CROSS_PRODUCT", "Cross Product (CP) VEC MATH"],
    [" VM PROJECT", "Project (P) VEC MATH"],
    [" VM REFRACT", "Refract (R) VEC MATH"],
    [" VM REFLECT", "Reflect (R) VEC MATH"],
    [" VM DOT_PRODUCT", "Dot Product (DP) VEC MATH"],
    [" VM DISTANCE", "Distance (D) VEC MATH"],
    [" VM MULTIPLY_ADD", "Multiply Add (MA) VEC MATH"],
    [" VM FACEFORWARD", "Faceforward (F) VEC MATH"],
    [" VM LENGTH", "Length (L) VEC MATH"],
    [" VM SCALE", "Scale (S) VEC MATH"],
    [" VM NORMALIZE", "Normalize (N) VEC MATH"],
    [" VM ABSOLUTE", "Absolute (A) VEC MATH"],
    [" VM MINIMUM", "Minimum (M) VEC MATH"],
    [" VM MAXIMUM", "Maximum (M) VEC MATH"],
    [" VM FLOOR", "Floor (F) VEC MATH"],
    [" VM CEIL", "Ceiling (C) VEC MATH"],
    [" VM FRACTION", "Fraction (F) VEC MATH"],
    [" VM MODULO", "Modulo (M) VEC MATH"],
    [" VM WRAP", "Wrap (W) VEC MATH"],
    [" VM SNAP", "Snap (S) VEC MATH"],
    [" VM SINE", "Sine (S) VEC MATH"],
    [" VM COSINE", "Cosine (C) VEC MATH"],
    [" VM TANGENT", "Tangent (T) VEC MATH"],
]

color = [
    [" C VALUE", "Value (V) COLOR"],
    [" C COLOR", "Color (C) COLOR"],
    [" C SATURATION", "Saturation (S) COLOR"],
    [" C HUE", "Hue (H) COLOR"],
    [" C DIVIDE", "Divide (D) COLOR"],
    [" C SUBTRACT", "Subtract (S) COLOR"],
    [" C DIFFERENCE", "Difference (D) COLOR"],
    [" C LINEAR_LIGHT", "Linear Light (LL) COLOR"],
    [" C SOFT_LIGHT", "Soft Light (SL) COLOR"],
    [" C OVERLAY", "Overlay (O) COLOR"],
    [" C ADD", "Add (A) COLOR"],
    [" C DODGE", "Dodge (D) COLOR"],
    [" C SCREEN", "Screen (S) COLOR"],
    [" C LIGHTEN", "Lighten (L) COLOR"],
    [" C BURN", "Burn (B) COLOR"],
    [" C MULTIPLY", "Multiply (M) COLOR"],
    [" C DARKEN", "Darken (D) COLOR"],
    [" C MIX", "Mix (M) COLOR"],
]

bool_math = [
    [" BM AND", "And (A) BOOL MATH"],
    [" BM OR", "Or (O) BOOL MATH"],
    [" BM NOT", "Not (N) BOOL MATH"],
    [" BM NAND", "Not And (NA) BOOL MATH"],
    [" BM NOR", "Nor (N) BOOL MATH"],
    [" BM XNOR", "Equal (E) BOOL MATH"],
    [" BM XOR", "Not Equal (NE) BOOL MATH"],
    [" BM IMPLY", "Imply (I) BOOL MATH"],
    [" BM NIMPLY", "Subtract (S) BOOL MATH"],
]

rand_val = [
    [" RV FLOAT", "Float (F) RAND VAL"],
    [" RV INT", "Integer (I) RAND VAL"],
    [" RV FLOAT_VECTOR", "Vector (V) RAND VAL"],
    [" RV BOOLEAN", "Boolean (B) RAND VAL"],
]

switch = [
    [" SW FLOAT", "Float (F) SWITCH"],
    [" SW INT", "Integer (I) SWITCH"],
    [" SW BOOLEAN", "Boolean (B) SWITCH"],
    [" SW VECTOR", "Vector (V) SWITCH"],
    [" SW STRING", "String (S) SWITCH"],
    [" SW RGBA", "Color (C) SWITCH"],
    [" SW OBJECT", "Object (O) SWITCH"],
    [" SW IMAGE", "Image (I) SWITCH"],
    [" SW GEOMETRY", "Geometry (G) SWITCH"],
    [" SW COLLECTION", "Collection (C) SWITCH"],
    [" SW TEXTURE", "Texture (T) SWITCH"],
    [" SW MATERIAL", "Material (M) SWITCH"],
]

sep_col = [
    [" SEP RGB", "RGB (SR) SEP RGB"],
    [" SEP HSV", "HSV (SH) SEP HSV"],
    [" SEP HSL", "HSL (SL) SEP HSL"],
]

com_col = [
    [" COM RGB", "RGB (CR) COM RGB"],
    [" COM HSV", "HSV (CH) COM HSV"],
    [" COM HSL", "HSL (CL) COM HSL"],
]

vec_rot = [
    [" VR AXIS_ANGLE", "Axis (VRA) VECTOR ROTATE"],
    [" VR X_AXIS", "X (VRX) VECTOR ROTATE"],
    [" VR Y_AXIS", "Y (VRY) VECTOR ROTATE"],
    [" VR Z_AXIS", "Z (VRZ) VECTOR ROTATE"],
    [" VR EULER_XYZ", "Euler (VRE) VECTOR ROTATE"],
]

uv_unwrap = [
    [" UU ANGLE_BASED", "Angle Based (AB) UV UNWRAP"],
    [" UU CONFORMAL", "Conformal (C) UV UNWRAP"],
]

fillet_curve = [
    [" FC BEZIER", "Bezier (B) FILLET CURVE"],
    [" FC POLY", "Poly (P) FILLET CURVE"]
]

dom_size = gen_non_dtype_subnodes("DS", "DOMAIN SIZE", COMPONENT)
geo_prox = gen_non_dtype_subnodes("GPX", "GEO PROX", TARGET_EL)
set_spline_type = gen_non_dtype_subnodes("SPT", "SET SPLINE TYPE", SPLINE_TYPE)
merge_by_dist = gen_non_dtype_subnodes("MbD", "MERGE BY DIST", ["ALL", "CONNECTED"])
mesh_boolean = gen_non_dtype_subnodes("MB", "MESH BOOLEAN", OPERATION)
dupe_el = gen_non_dtype_subnodes("DE", "DUPLICATE ELEM", DOMAIN[:3] + DOMAIN[-2:])
sep_geo = gen_non_dtype_subnodes("SG", "SEP GEO", DOMAIN[:3] + DOMAIN[-2:])
float_to_int = gen_non_dtype_subnodes("FtI", "FLOAT TO INT", ROUNDING_MODES)

named_attr = gen_dtype_subnodes("NA", "NAMED ATTR")

attr_stat = gen_subnodes("AST", "ATTR STAT", ["FLOAT", "FLOAT_VECTOR"], DOMAIN)
raycast = gen_subnodes("RAY", "RAYCAST", DATA_TYPE, MAPPING)
store_named_attr = gen_subnodes("STO", "STORE", DATA_TYPE, DOMAIN)
capture_attr = gen_subnodes("CAP", "CAP ATTR", DATA_TYPE, DOMAIN)
map_range = gen_subnodes("MR", "MAP RANGE", ["FLOAT", "FLOAT_VECTOR"], INTERPOLATION)
field_at_index = gen_subnodes("FaI", "FIELD AT INDEX", DATA_TYPE, DOMAIN)
scale_el = gen_subnodes("SE", "SCALE ELEMENTS", DOMAIN[1:-3], SCALE_EL_MODES)
accum_field = gen_subnodes("AF", "ACCUM FIELD", ["FLOAT", "INT", "FLOAT_VECTOR"], DOMAIN)

SUBNODE_ENTRIES = {
    "Math": math,
    "Vector Math": vec_math,
    "MixRGB": color,
    "Boolean Math": bool_math,
    "Random Value": rand_val,
    "Switch": switch,
    "Separate Color": sep_col,
    "Combine Color": com_col,
    "Domain Size": dom_size,
    "Geometry Proximity": geo_prox,
    "Set Spline Type": set_spline_type,
    "Merge by Distance": merge_by_dist,
    "Mesh Boolean": mesh_boolean,
    "Named Attribute": named_attr,
    "Attribute Statistic": attr_stat,
    "Raycast": raycast,
    "Store Named Attribute": store_named_attr,
    "Capture Attribute": capture_attr,
    "Map Range": map_range,
    "Separate Geometry": sep_geo,
    "Duplicate Elements": dupe_el,
    "Field at Index": field_at_index,
    "Scale Elements": scale_el,
    "Vector Rotate": vec_rot,
    "Compare": gn_cmp_vec + gn_cmp_fl_it + gn_cmp_col + gn_cmp_str,
    "UV Unwrap": uv_unwrap,
    "Filter": c_filter,
    "Float to Integer": float_to_int,
    "Accumulate Field": accum_field,
    "Fillet Curve": fillet_curve
}

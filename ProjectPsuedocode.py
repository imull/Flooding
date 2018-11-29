Yay!

#PART 0: Change Imagery Format [WILL BE DONE MANUALLY]
#Extract LEDAPS Images from .tar to .tiff. Output will be individual LEDAPS tiff raster files.

#PART 1: Import Imagery
#Import module & Environment
Import arcpy
Import os
arcpy.env.workspace = r’C:/Data/*name*.gdb’ 

#PART 1.5 to check-out Spatial Analyst 
#Check out arcpy spatial extension
arcpy.CheckOutExtension (“Spatial”)

#PART 2: Align & Clip Imagery
# Select raster area based upon Wilmington XY coordinate corners  (creating a polygon geometry object) [potentially better to use a Mask function?] 
# First, create empty point and array objects
pnt = arcpy.Point()
ary = arcpy.Array()
coordList = [ [X1,Y1], [X2,Y2], [X3,Y3], [X4,Y4] ]


# Loop through coordinate list pairs and populate point object
for coord in cordList:
pnt.x = coord [0]
	pnt.y = coord [1]
	# pass point to array
	ary.add(pnt)
polygon = arcpy.Polygon(ary)

# Confirm that data was added. Print to user the number of points created 
Print “Point Count: {0}”.format(polygon.pointcount)

# Use selection to clip Landsat imagery [Could possible use this code acquired from here and skip the above step to clip rasters to the Wilmington shapefile]. Once raster and shapefile are added to the file: 
Extents = arcpy.sa.Raster(MyRaster).extent`

# Use these lines to make a polygon out of these extents:
pnt_array = arcpy.Array()
pnt_array.add(Extents.lowerLeft)
pnt_array.add(Extents.lowerRight)
pnt_array.add(Extents.upperRight)
pnt_array.add(Extents.upperLeft)
poly = arcpy.Polygon(pnt_array)

# Clip my shapefile using this code. Outputs are raster which fit Wilmington’s boundary 
arcpy.Clip_analysis(shp, poly, Shp_clip)

#PART 2.5: Reproject rasters and shapefile to a projected coordinate system 
#Project a shapefile: Project_management (in_dataset, out_dataset, out_coor_system, transform_method, {in_coor_system}, {preserve_shape}, {max_deviation}, {vertical})
# Projected Coordinate System used: NAD_1983_StatePlane_North_Caroli
na_FIPS_3200 [WKID = 32119]
# set up paths to input and output directories
input_location = os.path.join(arcpy.env.workspace,'[OUR RASTER FILES LOCATION]')
output_location = os.path.join(arcpy.env.workspace,'ReProjected')
input_location_shapefile = os.path.join(arcpy.env.workspace,'[OUR Shapefile LOCATION]')
output_location_shapefile = os.path.join(arcpy.env.workspace,'ReProjected')
    
# get list of all input tifs
arcpy.env.workspace = input_location
# Get and print a list of GRIDs from the workspace
rasters = arcpy.ListRasters("*", "TIF")   # this only works in the current workspace (ANNOYING)
shapefiles = arcpy.ListFeatureClasses (“*”, “SHP”)

# iterate through all rasters and shapefile polygons in input directory, project, and write to output directory
for raster in rasters:
	# reproject a raster by appending input and output paths with raster names
	arcpy.ProjectRaster_management(in_raster=os.path.join(input_location, raster),
            	out_raster=os.path.join(output_location, raster), out_coor_system= “32119”)

for polygon in shapefiles:
	arcpy.Project_managment (in_dataset = input_location_shapefile = 				os.path.join(input_location_shapefile, polygon), out_dataset = os.path.join				(output_location_shapefile, polygon), out_coor_system = “32119”, transform method =		 ???)


#PART 3: Iterate & Classify
#Begin iteration for tiff files
for raster in RasterList:

#Supervised classification
#Calculate new raster values using NWDI (Normalized Difference Water Index). Output is a raster file with NWDI values for each cell.
#     (McFeeters, 1996) This formula is for detecting water bodies.
#ArcHelp link: http://desktop.arcgis.com/en/arcmap/10.3/tools/3d-analyst-toolbox/an-overview-of-the-raster-math-toolset.htm

arcpy.rastermath([inrastergreen, inrasterNIR], ‘((a - b)/(a + b))’, outrasNDWI_#])

#Before classification, create training samples and make .ecd (Esri Classifier Definition) file. #This will be input the the classification module to define the classification rules.
#Create a “water” classification based on pixels which are known water bodies. (We’re only doing water, nothing else). Merge similar signatures.

This is done manually using the Image Classification Toolbar and Training Sample Manager. This will create an .ecd file which can be plugged into the next step.

#Run Classifications. Output will be a classified raster file of Water and Not Water.
#ArcHelp link: http://desktop.arcgis.com/en/arcmap/10.3/tools/spatial-analyst-toolbox/train-maximum-likelihood-classifier.htm
In_training_features = raw_input(“Enter the Image Training File Name: “)
arcpy.TrainMaximumLikelihoodClassifier (in_raster, in_training_features, out_classifier_definition, {in_additional_raster}, {used_attributes})
#Accuracy Analysis?
#Add Raster Datasets Together (Mosaic to New Raster) to make one  full extent of flooding
#ArcHelp link: http://desktop.arcgis.com/en/arcmap/latest/tools/data-management-toolbox/mosaic-to-new-raster.htm
MosaicToNewRaster_management (input_rasters, output_location, raster_dataset_name_with_extension, {coordinate_system_for_the_raster}, {pixel_type}, {cellsize}, number_of_bands, {mosaic_method}, {mosaic_colormap_mode})
#Vectorize Data (Raster to Polygon). Output will be a multiple polygon feature classes
#ArcHelp link: http://desktop.arcgis.com/en/arcmap/latest/tools/conversion-toolbox/raster-to-polygon.htm
RasterToPolygon_conversion (in_raster, out_polygon_features, {simplify}, {raster_field}, {create_multipart_features}, {max_vertices_per_feature})
#Dissolve Water Polygons. This will merge the separate polygons into one feature class
#ArcHelp link: http://pro.arcgis.com/en/pro-app/tool-reference/data-management/dissolve.htm
Dissolve_management (in_features, out_feature_class, {dissolve_field}, {statistics_fields}, {multi_part}, {unsplit_lines})
#Part 4: Compare Flood Extent With FEMA maps 
#Import Hydrology layer, FEMA flood map layer, and the new Flood Polygon layer
Import arcpy
Import os
arcpy.env.workspace = r’C:/Data/*name*.gdb’ 
#Subtract known water bodies from Flood Polygon using Erase tool in the Overlay toolset. This will create a polygon of only flood waters.
#ArcHelp link: http://pro.arcgis.com/en/pro-app/tool-reference/analysis/erase.htm
Erase_analysis (in_features, erase_features, out_feature_class, {cluster_tolerance})

#Repeat Erase with FEMA Flood Map data to get full extent of flooding beyond FEMA flood maps. This will create a polygon of flooding beyond the FEMA lines.

#PART 5: Export Map (highlighting areas beyond FEMA boundaries which were flooded)
#ArcHelp link: http://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-mapping/exporttopdf.html

ExportToPDF Syntax: (map_document, out_pdf, {data_frame}, {df_export_width}, {df_export_height}, {resolution}, {image_quality}, {colorspace}, {compress_vectors}, {image_compression}, {picture_symbol}, {convert_markers}, {embed_fonts}, {layers_attributes}, {georef_info}, {jpeg_compression_quality})

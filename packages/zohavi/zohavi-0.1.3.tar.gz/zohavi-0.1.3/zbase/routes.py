import json
from pathlib import Path
  
from flask_classful import  FlaskView,  route 
from . import bp

from flask_login import current_user #,   login_required
from flask_classful import FlaskView, route
from flask import   send_file, current_app, render_template,  current_app , abort

class BaseView(FlaskView):
	route_base = '/'
	bpname = 'base'
	bp = bp

	##############################################################################################################
	#	Return any static resources
	##############################################################################################################
	@route('/st/<string:subdir_type>/<string:module>/<path:resourceFile>')
	def get_page(self, subdir_type, module, resourceFile):		
		# path = current_app.config['APP_BASE_DIR']
		path = current_app.config['ENV_BASE_DIR']
		if subdir_type in [ "_def", "app"]: 
			path += subdir_type + "/" 
		else:
			logger.error( f"incorrect type sent of:{subdir_type}")
			abort(500)

		send_file_path = path + module + "/" + resourceFile

 
		if Path(send_file_path).is_file():
			logger.debug("file found:" + str(send_file_path)   )
			return send_file(send_file_path)

		logger.error("file missing:" + str(send_file_path)   )
		abort(404)


	# def x__get_pagex(self, resourceFile):		
		
	# 	filename = self.bpname + '/static/' + resourceFile

	# 	default_path = current_app.config['RESOURCES_DEFAULTS_PATH'] +  filename
	# 	# default_path = current_app.config['DEFAULTS_PATH'] + '_def/' + filename
	# 	cust_path = current_app.config['RESOURCES_CUST_PATH']  + filename

	# 	send_file_path =  cust_path if Path(cust_path).is_file() else  default_path

	# 	# logger.debug()
	# 	logger.debug("**resourcefile:" + str(send_file_path) + ":" + self.bpname   )
	# 	logger.debug("path - default:" + str(default_path)   )
	# 	logger.debug("path - custom :" + str(cust_path)   )
	# 	logger.debug("path - final  :" + str(send_file_path)   )
		
	# 	# file_extension = Path(send_file_path).suffix

	# 	# if Path(send_file_path).suffix in ['.html', '.css']: 
	# 	# 	logger.debug("rendering: {}".format(resourceFile))
	# 	# 	return render_template(  resourceFile )
	# 	if Path(send_file_path).is_file():
	# 		return send_file(send_file_path)
	# 	abort(404)
	# 	# return send_file( bp.name + '/static/' + resourceFile  ) 



 	# ##############################################################################################################
	# #	Return any static resources
	# ##############################################################################################################
	# # @route('/file_config_path/<path:path_config_name>', methods=['GET', 'POST'], endpoint="file_config_path") 
	# @route('/file_config_path/<string:path_config_name>', methods=['GET', 'POST'], endpoint="file_config_path") 
	# def get_file_config_path(self, path_config_name):	

	# 	logger.debug(request.form)
	# 	file_path = self._get_file_config_path_internal(  path_config_name  )
	# 	if not file_path:
	# 		return json.dumps( {'error': f"Config path {path_config_name} not found"} ), 500
	# 	return json.dumps( {'path': file_path} ), 200

	# def _get_file_config_path_internal(self, config_path_name):
	# 	if 'FILE_ACCESS' in current_app.config and config_path_name in current_app.config['FILE_ACCESS']:
	# 		return current_app.config['BASE_DIR'] + current_app.config['FILE_ACCESS'][ config_path_name ]	
	# 	return None

	# ##############################################################################################################
	# #	Return any static resources
	# ##############################################################################################################
	# @route('/file_browse/<string:path_config_name>', methods=['GET', 'POST'], endpoint="file_browse")
	# #@route('/<path:resourceFile>', methods=['GET', 'POST'])
	# def get_file_data(self, path_config_name):	
	# 	# breakpoint()
	# 	logger.debug(request.form)

	# 	base_path = self._get_file_config_path_internal( path_config_name )
		
	# 	if base_path:
	# 		#concatenate the home base directory with the config relative path
	# 		search_path = base_path + request.form['path'] if( request.form['path'][:1] != '/' ) else base_path + request.form['path'][1:]

	# 		dirpath = Path( search_path  )
	# 		assert( dirpath.is_dir() )	
	#  		#create hash and label each record as either file or dir
	# 		file_list = [ {'name':x.name, 'type':'file' if x.is_file() else 'dir' }  for x in dirpath.iterdir()  ] 
	# 		return json.dumps( {'path': search_path, 'files': file_list} ), 200

	# 	return json.dumps( {'error': f"Config path {path_config_name} not found"} ), 500
'''
Created on 28 Oct 2021

@author: jacklok
'''

from flask import Blueprint 
import logging
from trexapi.decorators.api_decorators import auth_token_required
from trexlib.utils.string_util import is_not_empty, is_empty
from trexadmin.libs.http import create_rest_message
from trexadmin.libs.http import StatusCode
from trexmodel.models.datastore.pos_models import POSSetting
from trexmodel.utils.model.model_util import create_db_client
from flask.globals import request
from flask.helpers import url_for
from trexmodel.models.datastore.product_models import ProductCatalogue,\
    ProductCategory
from trexlib.utils.common.common_util import sort_list

#logger = logging.getLogger('api')
logger = logging.getLogger('debug')

pos_api_bp = Blueprint('pos_api_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/api/v1/pos')

@pos_api_bp.route('/check-activation', methods=['POST'])
def check_activation():
    activation_code = request.args.get('activation_code') or request.form.get('activation_code') or request.json.get('activation_code')
    logger.debug('activation_code=%s', activation_code)
    
    if is_not_empty(activation_code):
        db_client = create_db_client(caller_info="check_activation")
        with db_client.context():
            pos_setting = POSSetting.get_by_activation_code(activation_code)
        
        if pos_setting:
            if pos_setting.activated==False:
                return create_rest_message(status_code=StatusCode.OK)
            else:
                return create_rest_message('The code have been used to activate before', status_code=StatusCode.BAD_REQUEST)
        else:
            return create_rest_message('Invalid activate code', status_code=StatusCode.BAD_REQUEST)
    else:
        return create_rest_message('Activation code is required', status_code=StatusCode.BAD_REQUEST)

def getPOSAccountSetting(activation_code):
    if is_not_empty(activation_code):
        db_client = create_db_client(caller_info="getPOSAccountSetting")
        with db_client.context():
            pos_setting = POSSetting.get_by_activation_code(activation_code)
        
        if pos_setting:
            logger.info('Found POS setting');
            #if pos_setting.activated==False:
            if True:
                logger.info('POS activation code is valid');
                pos_setting_details = None
                with db_client.context():
                    #is_activated = POSSetting.activate(activation_code)
                    #if is_activated:
                    
                    pos_setting_details                                 = pos_setting.setting
                    
                    pos_setting_details['logo_image_url']               = url_for('system_bp.merchant_logo_image_url', merchant_act_key=pos_setting_details.get('account_id'))
                
                #if is_activated:
                if True:
                    
                    logger.debug('pos_setting_details=%s', pos_setting_details);
                    
                    return create_rest_message(status_code=StatusCode.OK,
                                               **pos_setting_details
                                               )
                else:
                    return create_rest_message('Failed to activate', status_code=StatusCode.BAD_REQUEST)
            else:
                logger.info('POS activation code have been used');
                return create_rest_message('The code have been used to activate before', status_code=StatusCode.BAD_REQUEST)
        else:
            logger.info('POS setting record is not found');
            return create_rest_message('Invalid activate code', status_code=StatusCode.BAD_REQUEST)
    else:
        logger.info('activation_code is empty');
        return create_rest_message('Activation code is required', status_code=StatusCode.BAD_REQUEST)
    
    
@pos_api_bp.route('/activate', methods=['POST'])
@pos_api_bp.route('/account-sync', methods=['get'])
def activate():
    activation_code = request.args.get('activation_code') or request.form.get('activation_code') or request.json.get('activation_code')
    
    logger.debug('activation_code=%s', activation_code)
    return getPOSAccountSetting(activation_code)
       
    
def parse_category_to_json(category_tree_structure):
    data_list = []
    
    for category in category_tree_structure:
        data = {
                    'code'                  : category.get('key'),
                    'label'                 : category.get('category_label'),
                    'label_with_item_count' : category.get('category_label_and_other_details'),
                    'group'                 : category.get('has_child'),
                    'product_modifier'      : category.get('product_modifier'),
                    'product_items'         : category.get('product_items'),
                }
        if category.get('childs'):
            child_data_list = parse_category_to_json(category.get('childs'))
            if child_data_list:
                data['childs'] = child_data_list   
        
        data_list.append(data)
    
    return data_list

def construct_category_tree_structure(category_tree_structure, category_list):
    for category in category_list:
        if is_empty(category.get('parent_category_key')):
            #top most category
            category_tree_structure.append(category)
            __find_child_category(category, category_list)
                

def __lookup_category_from_category_list(category_code, category_list):
    for category in category_list:
        if category.get('key') == category_code:
            return category  

    
def __find_child_category(category, category_list):
    if is_not_empty(category.get('child_category_keys')):
        childs                      = []
        parent_product_modifier     = category.get('product_modifier') or []
        
        for child_category_key in category.get('child_category_keys'):
            child = __lookup_category_from_category_list(child_category_key, category_list)
            
            logger.debug('category product_modifier of %s =%s', category.get('key'), parent_product_modifier)
            if child:
                child_product_modifier      = child.get('product_modifier') or []
                child_product_modifier      = list(set(parent_product_modifier) | set(child_product_modifier) )
                child['product_modifier']   = child_product_modifier
                
                logger.debug('child_product_modifier of %s =%s', category.get('key'), child_product_modifier)
                
                if is_not_empty(child.get('child_category_keys')):
                    __find_child_category(child, category_list)
                childs.append(child)
        
        category['childs'] = childs

def get_product_category_structure_code_label_json(merchant_acct):
    category_list       = get_product_category_structure(merchant_acct)
    
    category_tree_structure = []
    
    construct_category_tree_structure(category_tree_structure, category_list)
    
    return parse_category_to_json(category_tree_structure)

def get_product_category_structure(merchant_acct):
    
    sorted_category_structure = []
    
    category_structure      = ProductCategory.get_structure_by_merchant_acct(merchant_acct)
    category_structure      = sort_list(category_structure, sort_attr_name='category_label')
    
    #logger.debug('category_structure=%s', category_structure)
    
    for c in category_structure:
        sorted_category_structure.append(c.to_dict())
    
    
    logger.debug('sorted_category_structure=%s', sorted_category_structure)
            
    return sorted_category_structure

@pos_api_bp.route('/check-catalogue-status', methods=['GET'])
@auth_token_required
def check_catalogue_status():
    activation_code = request.args.get('activation_code') or request.form.get('activation_code') or request.json.get('activation_code')
    
    if is_not_empty(activation_code):
        pos_setting = None
        db_client = create_db_client(caller_info="check_catalogue_status")
        with db_client.context():
            pos_setting = POSSetting.get_by_activation_code(activation_code)
            if pos_setting:
                
                assigned_outlet = pos_setting.assigned_outlet_entity
                
                catalogue_key   = assigned_outlet.assigned_catalogue_key
                
                if is_not_empty(catalogue_key):
                    product_catalogue   = ProductCatalogue.fetch(catalogue_key)
                    if product_catalogue:
                        return {
                                    'last_updated_datetime' : product_catalogue.modified_datetime.strftime('%d-%m-%Y %H:%M:%S')
                                } 
                    else:
                        return create_rest_message('Invalid catalogue data', status_code=StatusCode.BAD_REQUEST)
        
        if pos_setting is None:
            return create_rest_message('Invalid activation code', status_code=StatusCode.BAD_REQUEST)
        else:
            return create_rest_message('Not catqalogue have been assigned or published', status_code=StatusCode.BAD_REQUEST)
                
    else:
        return create_rest_message('Activation code is required', status_code=StatusCode.BAD_REQUEST)
    
@pos_api_bp.route('/get-catalogue', methods=['GET'])
@auth_token_required
def get_catalogue():
    activation_code = request.args.get('activation_code') or request.form.get('activation_code') or request.json.get('activation_code')
    
    logger.debug('activation_code=%s', activation_code);
    
    if is_not_empty(activation_code):
        pos_setting         = None
        db_client           = create_db_client(caller_info="get_catalogue")
        valid_return        = None
        product_catalogue   = None
        with db_client.context():
            pos_setting = POSSetting.get_by_activation_code(activation_code)
            if pos_setting:
                
                assigned_outlet = pos_setting.assigned_outlet_entity
                
                logger.info('assigned_outlet name=%s', assigned_outlet.name)
                
                catalogue_key   = assigned_outlet.assigned_catalogue_key
                
                logger.debug('catalogue_key=%s', catalogue_key);
                
                if is_not_empty(catalogue_key):
                    product_catalogue   = ProductCatalogue.fetch(catalogue_key)
                    merchant_acct       = pos_setting.merchant_acct_entity
                    
                    #category_tree_structure_in_json  = json.dumps(get_product_category_structure_code_label_json(merchant_acct), sort_keys = True, separators = (',', ': '))
                    category_tree_structure_in_json  = get_product_category_structure_code_label_json(merchant_acct)
                    
                    if product_catalogue:
                        last_updated_datetime = product_catalogue.modified_datetime
                        if assigned_outlet.modified_datetime is not None and assigned_outlet.modified_datetime>last_updated_datetime:
                            last_updated_datetime = assigned_outlet.modified_datetime
                        '''
                        dinning_option_json = []
                        dinning_option_list = DinningOption.list_by_merchant_acct(merchant_acct)
                        
                        
                        if dinning_option_list:
                            for d in dinning_option_list:
                                dinning_option_json.append({
                                                            'option_key'                : d.key_in_str,
                                                            'option_name'               : d.name,
                                                            'is_default'                : d.is_default,
                                                            'dinning_table_is_required' : d.dinning_table_is_required,
                                                            'assign_queue'              : d.assign_queue,
                                                            })
                        '''        
                        valid_return =  {
                                                'category'              : category_tree_structure_in_json,
                                                'menu'                  : product_catalogue.published_menu_settings,
                                                #'dinning_table_list'    : assigned_outlet.assigned_dinning_table_list,
                                                #'dinning_option_list'   : dinning_option_json,
                                                'last_updated_datetime' : last_updated_datetime.strftime('%d-%m-%Y %H:%M:%S')
                                            } 
                    
                
                    
        if valid_return:
            return valid_return
        else:
            if product_catalogue==None:
                logger.debug('No catalogue have been assigned or published');
                return create_rest_message('No catqalogue have been assigned or published', status_code=StatusCode.BAD_REQUEST)
            else:
                if pos_setting is None:
                    logger.debug('Invalid activation code');
                    return create_rest_message('Invalid activation code', status_code=StatusCode.BAD_REQUEST)
                else:
                    logger.debug('No catalogue have been assigned or published');
                    return create_rest_message('No catqalogue have been assigned or published', status_code=StatusCode.BAD_REQUEST)
                
    else:
        return create_rest_message('Activation code is required', status_code=StatusCode.BAD_REQUEST)    

@pos_api_bp.route('/version-sync', methods=['get'])
def version_sync():
    db_client       = create_db_client(caller_info="version_sync")
    
    with db_client.context():
        version =  {
                                '''
                                'setting':[
                                            {
                                                "table_name": "setting",
                                                "version" : 1,
                                                "script": "ALTER TABLE setting ADD COLUMN account_settings TEXT",
                                            }
                                               
                                        ],
                                'user'  :[
                                            {
                                                "table_name": "user",
                                                "version" : 1,
                                                "script": "ALTER TABLE user ADD COLUMN token_expiry_datetime TEXT",
                                                
                                            }
                                        ]
                                '''        
        
                                'cart'  :[
                                            {
                                                "table_name": "cart",
                                                "version" : 1,
                                                "script": "ALTER TABLE invoice ADD COLUMN void_by TEXT",
                                                
                                            }
                                        ]
                            }
                                
    
            
    
    return version


     
           

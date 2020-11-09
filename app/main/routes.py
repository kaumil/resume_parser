from app.main import bp

@bp.route('/health',methods=['GET'])
def health_check():
    '''
        Function to send health check for target group
    '''
    return {"result": "Healthy"}, 200
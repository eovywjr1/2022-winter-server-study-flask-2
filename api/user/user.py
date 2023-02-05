from flask import Flask, request, jsonify
from flask_restx import Resource, Namespace
from database.database import Database

user = Namespace('user')
Database.close()
db = Database()

@user.route('')
class UserManagement(Resource):
    def get(self):
        """유저 데이터 조회"""
        
        userInfo = request.args.to_dict()
        id = userInfo['id']
        password = userInfo['password']
        
        sql = "SELECT count(*) FROM user WHERE id = '" + id + "'"
        row = db.execute_one(sql)
        if(row[0] == 0): return jsonify({'message' : '해당 유저가 존재하지 않음'}), 400
        else:
            sql = "SELECT count(*) FROM user WHERE id = '" + id + "' and pw = '" + password + "'"
            row = db.execute_one(sql)
            
            if(row[0] == 0): return jsonify({'message' : '아이디나 비밀번호 불일치'}), 400
            else: return jsonify({'nickname' : row[2]}), 200
    
    def post(self):
        """유저 생성"""
        
        userInfo = request.get_json()
        id = userInfo['id']
        password = userInfo['password']
        nickname = userInfo['nickname']
        
        sql = "SELECT count(*) FROM user WHERE id = '" + id + "'"
        row = db.execute_one(sql)
        if(len(row) == 0):
            sql = "INSERT INTO user VALUES ('" + id + "', '" + password + "', '" + nickname + "')"
            db.execute(sql)
            
            return jsonify({'is_success' : True, 'message' : '유저 생성 성공'}), 200
        else: return jsonify({'is_success' : False, 'message' : '이미 있는 유저'}), 400

    def put(self):
        """유저 데이터(닉네임) 수정"""
        
        userInfo = request.get_json()
        id = userInfo['id']
        password = userInfo['password']
        nickname = userInfo['nickname']
        
        sql = "SELECT count(*) FROM user WHERE id = '" + id + "' and pw = '" + password + "'"
        row = db.execute_one(sql)
        if(row[0] == 0): return jsonify({'is_success' : False, 'message' : '아이디나 비밀번호 불일치'}), 400
        elif(row[2] == nickname): return jsonify({'is_success' : False, 'message' : '현재 닉네임과 같음'}), 400
        else:
            sql = "UPDATE user SET nickname = '" + nickname + "' WHERE id = '" +  id + "'"
            db.execute(sql)
            
            return jsonify({'is_success' : True, 'message' : '유저 닉네임 변경 성공'}), 200
    
    def delete(self):
        """유저 삭제"""
        
        userInfo = request.get_json()
        id = userInfo['id']
        password = userInfo['password']
        
        sql = "SELECT count(*) FROM user WHERE id = '" + id + "' and pw = '" + password + "'"
        row = db.execute_one(sql)
        if(row[0] == 0): return jsonify({'is_success' : False, 'message' : '아이디나 비밀번호 불일치'}), 400
        else:
            sql = "DELETE FROM user WHERE id = '" + id + "'"
            db.execute(sql)
            
            return jsonify({'is_success' : True, 'message' : '유저 삭제 성공'}), 200
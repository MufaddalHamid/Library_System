import uuid
from DataModel.Members import Members
from BusinessLogic.AppHelper import ActiveSession
class MemberBC:
    def __init__(self, SysId=None):
        self.SysId = SysId
        self.load_member()

    def load_member(self):
        try:
            if self.SysId is not None:
                self.member = ActiveSession.Session.query(Members).filter_by(SysId=self.SysId).first()
            else:
                print('SysId not provided, initialized empty Member')
                self.member = Members()
        except Exception as e:
            print(f"Error loading Member data: {str(e)}")
            self.member = None

    def create_member(self,new_data):
        try:
            self.member = Members(**new_data)
            self.member.SysId = str(uuid.uuid4())
            Member_exists = ActiveSession.Session.query(Members).filter_by(email=self.member.email).first()
            if Member_exists:
                raise ValueError('Member Already Exists!!')
            else:
                ActiveSession.Session.add(self.member)
                ActiveSession.Session.commit()
                new_data['message'] = 'Member created successfully ' + str(self.member.Name)
                new_data['Code'] = 201
                return new_data
        except ValueError as ve:
            ActiveSession.Session.rollback()
            new_data['message'] = str(ve)
            new_data['Code'] = 500
            return new_data
        except Exception as e:
            ActiveSession.Session.rollback()
            new_data['message'] = str(e)
            new_data['Code'] = 500
            return new_data

    def get_members(self):
        try:
            print('called here')
            if self.SysId is None:
                return ActiveSession.Session.query(Members).all()
            else:
                if self.member:
                    return self.member
                else:
                    return {"error": "Member not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def update_member(self, new_data):
        try:
           if self.member is not None:
                for key, value in new_data.items():
                    setattr(self.member, key, value)
                ActiveSession.Session.commit()
                return {"message": "Member updated successfully ","Code":201}
           else:
               return {"message": "Member not found",'Code':404}
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e),'Code':500}

    def delete_member(self):
        try:
            ActiveSession.Session.delete(self.member)
            ActiveSession.Session.commit()
            return {"message": "Member deleted successfully",'Code':201 }
        except Exception as e:
            ActiveSession.Session.rollback()
            return {"message": str(e),'Code':500}


#-*- coding:utf8 -*-
'''
Created on 2014年5月20日

@author: Administrator
'''

import sys



if __name__ == '__main__':
    usage = 'you can use the following commands \n' + 'Command\t\t\t\t\tDetail'
    use1 = 'login\t\t\t\t\t login'
    use2 = 'who\t\t\t\t\t current user'
    use3 = 'upload [filename] [filepath]\t\t upload the file'
    use4 = 'download [remote_name][local_name]\t download the file'
    use5 = 'clear\t\t\t\t\t clear the user content'
    length = len(sys.argv)
    if length <= 1:
        print usage
        print use1
        print use2
        print use3
        print use4
        print use5
    else:
        command = sys.argv[1]
        if command == 'login':
            import AuthorizePhase
        elif command == 'who':
            import User
            User.who()
        elif command == 'clear':
            from User import clear
            clear()
        elif command == 'upload':
            if length < 4:
                print use3
            else:
                import UploadPhase
                UploadPhase.getAddress()
                UploadPhase.Upload(sys.argv[2],sys.argv[3])
        elif command == 'download':
            if length < 4:
                print use4
            else:
                import DownloadPhase
                print sys.argv[2]
                print sys.argv[3]
                DownloadPhase.download(sys.argv[2], sys.argv[3])
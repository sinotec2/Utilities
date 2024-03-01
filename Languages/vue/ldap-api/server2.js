const express = require('express');
const fileUpload = require('express-fileupload');
const favicon = require('express-favicon');

const cors = require('cors');
const bodyParser = require('body-parser');
const ldap = require('ldapjs');
const path = require('path');
const serveStatic = require('serve-static');

const { getUserAttributes } = require('./ldapUtils');

const app = express();
const port = 3000;
const ldapBase = 'dc=sinotech-eng,dc=com';

app.use(cors({ credentials: true, origin: 'http://200.200.32.195:8084' }));
app.use(serveStatic(path.join(__dirname, 'my-vue-project/dist')));
app.use(bodyParser.json());
app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy', 'default-src \'self\' http://200.200.32.195:3000/api/login'); 
  next();
});
app.use(fileUpload());


const ldapServer = 'ldap://200.200.31.47:389';

app.post('/api/login', async (req, res) => {
  console.log('Received login request:', req.body);
  const { username, password } = req.body;
  const userDn = `uid=${username},cn=users,cn=accounts,${ldapBase}`;
  console.log(`username,password:${username} ${password}`);

  const client = ldap.createClient({
    url: ldapServer
  });

  try {
    client.bind(userDn, password, (err) => {
      if (err) {
        console.error('LDAP authentication failed:', err);
        res.status(401).json({ message: 'LDAP authentication failed' });
      } else {
        console.log('LDAP authentication passed:', username);
        // 在這裡呼叫處理上傳檔案畫面的函式或路由
        res.status(200).json({ message: 'LDAP authentication successful' });
      }
   });
 } catch (error) {
   console.error('Error during LDAP authentication:', error);
   res.status(500).json({ message: 'Internal server error' });
   }
});

app.post('/api/upload', (req, res) => {
  if (!req.files || Object.keys(req.files).length === 0) {
    return res.status(400).send('No files were uploaded.');
  }

  const uploadedFile = req.files.file;

  const filePath = '/tmp/' + uploadedFile.name;
  uploadedFile.mv(filePath, (err) => {
    if (err) {
      return res.status(500).send(err);
    }

    res.send('File uploaded!');
  });
});


app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});



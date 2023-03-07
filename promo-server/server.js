import { xbl, authenticate } from '@xboxreplay/xboxlive-auth';
import express from 'express'


const deviceTokenResponse = await xbl.EXPERIMENTAL_createDummyWin32DeviceToken();
const { Token: deviceToken } = deviceTokenResponse;

const app = express()
app.use(express.json())
app.listen(1338, () => console.log("listening on 1338"));
app.post("/", async function (req, res) {
    try {
        var x = await authenticate(req.body.user, req.body.pass, { deviceToken }); 
    } catch (e) {
        console.log(e);
        res.json("error");
        return;
    }
    var token = `XBL3.0 x=${x.user_hash};${x.xsts_token}`;
    return res.json(token)
});

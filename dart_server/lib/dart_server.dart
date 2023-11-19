import 'package:encrypt/encrypt.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:pointycastle/asymmetric/api.dart';
import 'package:crypto/crypto.dart';

import 'package:encrypt/encrypt.dart' as enc;

String asymmetricEncrypt(String message, String key) {

  RSAKeyParser keyParser = RSAKeyParser();

  RSAAsymmetricKey publicKeyParser = keyParser.parse(key);

  final publicKey = RSAPublicKey(publicKeyParser.modulus!, publicKeyParser.exponent!);

   enc.Encrypter encrypter = enc.Encrypter(enc.RSA(publicKey: publicKey,  encoding: enc.RSAEncoding.PKCS1));

   enc.Encrypted msg = encrypter.encrypt(message);

   return msg.base64;
   
 }

Encrypter createFernetEncrypter(String username, String deviceID) {

  String key = username + deviceID;

  var byte = sha256.convert(utf8.encode(key)).bytes;

  final b64key = Key.fromBase64(base64Url.encode(byte));

  Fernet fernet = Fernet(b64key);
  enc.Encrypter encrypter = enc.Encrypter(fernet);

  return encrypter;
}

void main(List<String> arguments) async {

  var header = {'Content-Type': "application/json"};

  var body = jsonEncode(
    {
      'message': 'secret message',
      'username' : 'nednod',
      'deviceID' : 'aufh98qrh28',
      }
    );

  var sads = await http.post(Uri.parse('http://127.0.0.1:5000/register'), body: body, headers: header);

  // create encrypter
  enc.Encrypter encrypter = createFernetEncrypter("nednod", "aufh98qrh28");
  
  // convert encrypted json to Encrypted Type
  enc.Encrypted encryptedMsg = enc.Encrypted.from64(ascii.decode(base64Decode(sads.body)));

  // decode
  var decrypted = encrypter.decrypt(encryptedMsg);

  var js = jsonDecode(decrypted);
  var body2 = jsonEncode({'message': 'secret message'});
  
  var encrypted = asymmetricEncrypt(body2, js["key"]);

  var result = await http.post(Uri.parse('http://127.0.0.1:5000/decrypt'), body: encrypted, headers: header);

  print(result.body);

}
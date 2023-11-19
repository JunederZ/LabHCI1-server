import 'package:encrypt/encrypt.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:pointycastle/asymmetric/api.dart';

import 'package:encrypt/encrypt.dart' as enc;

 String asymmetricEncrypt(String message, String key) {

  RSAKeyParser keyParser = RSAKeyParser();

  RSAAsymmetricKey publicKeyParser = keyParser.parse(key);

  final publicKey = RSAPublicKey(publicKeyParser.modulus!, publicKeyParser.exponent!);

   enc.Encrypter encrypter = enc.Encrypter(enc.RSA(publicKey: publicKey,  encoding: enc.RSAEncoding.PKCS1));

   enc.Encrypted msg = encrypter.encrypt(message);

   return msg.base64;
   
 }

void main(List<String> arguments) async {

  var header = {'Content-Type': "application/json"};

  var sads = await http.get(Uri.parse('http://127.0.0.1:5000/register'), headers: header);

  var js = jsonDecode(sads.body);
  var body = jsonEncode({'message': 'secret message'});
  
  var encrypted = asymmetricEncrypt(body, js["key"]);

  var result = await http.post(Uri.parse('http://127.0.0.1:5000/decrypt'), body: encrypted, headers: header);

  print(result.body);

}

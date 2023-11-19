import 'package:encrypt/encrypt.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:pointycastle/asymmetric/api.dart';
import 'package:crypto/crypto.dart';

import 'package:encrypt/encrypt.dart' as enc;

String asymmetricEncrypt(String message, String key) {
  RSAKeyParser keyParser = RSAKeyParser();

  RSAAsymmetricKey publicKeyParser = keyParser.parse(key);

  final publicKey =
      RSAPublicKey(publicKeyParser.modulus!, publicKeyParser.exponent!);

  enc.Encrypter encrypter = enc.Encrypter(
      enc.RSA(publicKey: publicKey, encoding: enc.RSAEncoding.PKCS1));

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
  enc.Encrypter encrypter = createFernetEncrypter("asdf", "");

  String tode =
      "Z0FBQUFBQmxXb000TTlya2NxNjdBbDRLa0pKNEJabl9rQkhBeFVfaWF1eE1qbjB1Ui1hRVQtdGZaUG9zdnkzOGdreThDQWNmZzVtUk1XLXJidFdndVhHZ2pNQ0IyUkRRbnJTd3huS3dObzc4WXkteU5vR0thbi1mb2JzazlJYUhPcHFVNnJ0enJOLXlHb3pXazhySGZZZWdYRVNFM2VTbkhWcllDOVNMRkthT3hvTEtSVmR3YlhfNjZtY0ZTZjJjeFNUbFJEazAxZEV3bHBfWFlReGVKV09OaU5RZWFyYzFjbVZZUGtVdFVHMWZZOWtmUkFMVW5zUVVPUzR0NkJUVk1xV0lRTEQ3NnVLR2VITHQ3Zm9jcVN5bGkyRTEyZlBRUUltWkxMWFFCak9NR3lfTXNINWl4NFdOTll6UDhPUG9tQkhYVl9yYmhLd2FYakhNOWE0ZDlIS1U4NEt4WGNIWTRfeGdLQklRc0pvcHlSeVFpNzZmMWM0Mm1GMElTUUNQd1RnUURjZGFwdlQ0U2xtVGZkd0pxV2xra2pwRDFXSjVicWpZZEZTV19wODlUTmUxQ2dyYzFOcFltdElJSHZBU25heFoza285SkxJRWZ1U2FDT2g5cXVQWVVyZWNTMVZvUEhrN0dDbEZwVzIxOHNXVkdkTGVXYWk2VzhEdWgtUXQwTkE0WjVMV1MzN1ZHQ253dFJSaTFYMC1pNENMalZBdEd0cFJ4QWlKaEt1S0VpTkVMRXJjMzJ2UF9SWG9iV0VhU1EzUzh3T2ZBWWdnd1NxQVZJYlNfSVloTEpIejJtNktPSWtadlc2NldPdWxvYWVWaWZBRWJ2ZDlwM1owZXl5d1M1ZHc5eW9zeUlpU0ZWM2dlVDc3cXFicXhFaXJTQndsU1Q0WVpxNUxtNlhhY2VHMmstNUZ4Y0ZneDZXTWI2R0pTS3VUWFNRTEp3N3hWMjZiV1NxLUxMRWs1M2EtZTlOUDcwS1ZJcXJIeHg3X21xWkRTQkV2RFVlbmE2cEZvUm1Xd1ZUZDJZWUdSOWFJMjlKSVdPNm1FTWdHb1VvZ3dnV082MXhnTjFDVVYxa3kwVjFDbzlBazI1S3ZsVHhoa29NWVRKOGdaV2lBeUhKeU81aUg2a3pFcUt5YmRYcHV6c082NGN2ZzlpanNCc3V0OWxoSFRNX1VaYlBndm1UbjdGMFJQOWVuTUdicnpkNnQwU00teXRQbFA2dlZyWU9QdzNDeW1jcWJJY0dOY0FWS2NBU0stZzgtMURkbFFXSExKaXNfd2FNenE1VlRwQnoySXpOb2lOek5JN1I1blRRaXdBMjllMFBkRHo3ZmpoVVVURGZNMXJDeERWTWkxa1BLUnQxcHBzdHRvX1FpZHpaUDhFRExXUi1KSDl1Rnc1VDlvaFZWekJYU0hGQnQtbGYwUDJ3ZG4yd0UyLUdYbk5OR0QtRVpiaUliOE4tNHM4N1B4WmNTMjhuQmZ1MDBBTlU0Uk5oTVFCQm1YTHZRUlcwSDRPZXpFV09GTGRkMWdlQ1N1aGhGaGVkZ1dFazJScE90bE56NkNWMTRCSGdhMjFhenVJaGFNZz09";

  enc.Encrypted encryptedMsg =
      enc.Encrypted.from64(ascii.decode(base64Decode(tode)));

  var decrypted = encrypter.decrypt(encryptedMsg);
  print(decrypted);
  // String replaced = decrypted.replaceAll(r'\', r'\\');
  // print(replaced);
  var js = jsonDecode(decrypted);
  var body2 = jsonEncode({'message': 'secret message'});
  print(js);

  var encrypted = asymmetricEncrypt(body2, js["key"]);
  print(encrypted);

  // var result = await http.post(Uri.parse('http://127.0.0.1:5000/decrypt'),
  //     body: encrypted, headers: header);

  // print(result.body);
}

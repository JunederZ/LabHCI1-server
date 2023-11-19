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
  enc.Encrypter encrypter = createFernetEncrypter("ktsabit", "");

  String tode =
      "Z0FBQUFBQmxXbnYyUlJhak84TzdETVF1SW5hYUFSaV91ZU1QcFFhbFJvbTFoUk1wZWRSWGxjelhuQ2V1dHFaTG9kVFRla3VJX2RwTEVzMDlrY3UwdElGTHoteVJRVVNqM0FzLXZYN3M5ck1DRjBSUTVXR2VaVDFlUHJnMUxVaWJWQVRwTkNYaUpXVFgxME4xbkt0NEFyTExKdmRkSk5wd1JRVW5lRzVZeXdxWll4SGROYkNDWjZsc3hjQlRfXzhLU0prYjdubFdDU0VyX3pzNTd1bE81elRPSVhqcDhIREljQmZhcUlCZGRkSnd2R3h2Q1p5LVhoXzczWjcyc25zVnpxXzktcEZ5VW10SXBTYzBmLUlxLXFIeXJsal93MmNtT2lEdjVTUmlYM3VDbXA2clBabTZxSklhYTRJT2pmRzYzVjVMNkowcm81OENKMkU3TnJJRkJsWlNzcDVYcTc3NHJYUk4weUdwbG82MlhlOFUxaGszVGVabDZ0dUxkNXRITUFBRUdvdGt6em9feDVjZ1pUNEttYVpnNDBvNXJfdlpTM2FzRDUya2dLVmpWUmlRZWE0OHRudmdrbE9VSmdCaUpIMlVFYk1vQ29hV2JXN2lRV055U0ZYeVpmbWdTR2dLVW9BYmdWcC1uMFhsbXBHREdINXZic0hYSEwyWEpXOFlpZUxWMDU3OEQxV3NTQjVaOUZWOGpDMnpmcUJSS2xneEZCaGRjOEw2UFIzUTZETTFiTFFxaGRHLTJYbllSY2YxS21va0poNlYzWFp6WTE5Q3FBQjRnc2hkY0FLdm9HbEg3aFpfemdwMGpCUFRLdXphbVU4ME5MS21va0I0blAzX1JMMGUtSU9lSnNFcVgwNHcwa1FSS3pEY1NWTnlWMG1SRjlBNXFSRFhxb3Y3azZ2VmktSjlTVFBTYTNHbkxvblRUc2Z2NnktblhuNFlFRXV1dVUwMkV2N1U2TjhGelF1NFpLWjFGNDdQaVBtVEttLXczRG5JVWhYNnhoVlhhMWp4TXBQNE5fbWtxZ19MUDlHenFBb3VlQjlNWFJhMHUzOC1GSS0wZUJiUHhCMXBFcWRZX0h0bFVjR0hPZjV2MmZScnVFSGQ2anVrYjI5bWdscTRmVVlaSC1DTEgzbjRXZS1vVERreU9JU29FWURwZEcxeUJhUUd0TEUyQVpjeFVqTFZnekt1SWQtYVJZa2U2NnhPYW5ReG8yck5xakJKNG83Z2ZlYklZSjRtUy05TnpTWENXeVpPeUgxTGNjS00xRHlkWlJPU0oyd2VmbG5FSzkwZjllZmFSLVExYXAxRUFORy15eHNRQTJmTlpkQVh6TllLWGcyU01tVno5MUNPOUhYSHpCMk1HekNPTkRWem5EV3IyMV83RFRQc05talNKMTlaWFpOSlBkeWJneDVlamtXVW5TaXNacXNFSDUtNGxMOFJJT3VJNG5jbXYya3I2d1pCUEhRSGZKYlZLMzY0RXNQWm5lRXp6N1dzR2NjQTVBNVVrSlFldHRzX2JGUjNVY2xMWENhUDlYTGRINk5tY1MwN3V5dzlSd3ppNno3WWtxbXJsdFNfMU1mdWFGeXNSV1NFZXFzS2ZvND0=";

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

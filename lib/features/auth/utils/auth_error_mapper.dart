import '../../../generated/app_localizations.dart';

abstract final class AuthErrorMapper {
  static String fromSignInCode(AppLocalizations loc, String code) => switch (code) {
    'user-not-found'    => loc.authErrorUserNotFound,
    'wrong-password'    => loc.authErrorWrongPassword,
    'invalid-email'     => loc.invalidEmail,
    'user-disabled'     => loc.authErrorUserDisabled,
    'too-many-requests' => loc.authErrorTooManyRequests,
    _                   => loc.authErrorGeneric,
  };

  static String fromRegisterCode(AppLocalizations loc, String code) => switch (code) {
    'email-already-in-use' => loc.authErrorEmailInUse,
    'invalid-email'        => loc.invalidEmail,
    'weak-password'        => loc.authErrorWeakPassword,
    _                      => loc.authErrorAccountCreation,
  };
}

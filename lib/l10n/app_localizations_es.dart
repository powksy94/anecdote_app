// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Spanish Castilian (`es`).
class AppLocalizationsEs extends AppLocalizations {
  AppLocalizationsEs([String locale = 'es']) : super(locale);

  @override
  String get appTitle => 'Hechos del día';

  @override
  String get chooseCategory => 'Elige tu categoría';

  @override
  String get showDetails => 'Ver detalles';

  @override
  String get hideDetails => 'Ocultar detalles';

  @override
  String get unableToLoad => 'No se puede cargar el contenido';

  @override
  String get retry => 'Reintentar';

  @override
  String newContentIn(String time) {
    return 'Nuevo contenido en $time';
  }

  @override
  String get categoryAnecdote => 'Anécdota';

  @override
  String get categoryChuckNorris => 'Chuck Norris';

  @override
  String get categoryAdvice => 'Consejo';

  @override
  String get categoryHistory => 'Historia';

  @override
  String get categoryAnimals => 'Animales';

  @override
  String get showAnecdote => 'Mostrar anécdota';

  @override
  String get translate => 'Traducir al español';

  @override
  String get tapToHide => 'Toca de nuevo para ocultar los detalles';

  @override
  String get error => 'Error';

  @override
  String get translationError => 'Error de traducción';

  @override
  String get english => 'Inglés';

  @override
  String get french => 'Francés';

  @override
  String get spanish => 'Español';
}

import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_en.dart';
import 'app_localizations_es.dart';
import 'app_localizations_fr.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'generated/app_localizations.dart';
///
/// return MaterialApp(
///   localizationsDelegates: AppLocalizations.localizationsDelegates,
///   supportedLocales: AppLocalizations.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```yaml
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # Rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the AppLocalizations.supportedLocales
/// property.
abstract class AppLocalizations {
  AppLocalizations(String locale)
      : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates =
      <LocalizationsDelegate<dynamic>>[
    delegate,
    GlobalMaterialLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
  ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('en'),
    Locale('es'),
    Locale('fr')
  ];

  /// No description provided for @appTitle.
  ///
  /// In en, this message translates to:
  /// **'Daily Facts'**
  String get appTitle;

  /// No description provided for @chooseCategory.
  ///
  /// In en, this message translates to:
  /// **'Choose your category'**
  String get chooseCategory;

  /// No description provided for @showDetails.
  ///
  /// In en, this message translates to:
  /// **'Show details'**
  String get showDetails;

  /// No description provided for @hideDetails.
  ///
  /// In en, this message translates to:
  /// **'Hide details'**
  String get hideDetails;

  /// No description provided for @unableToLoad.
  ///
  /// In en, this message translates to:
  /// **'Unable to load content'**
  String get unableToLoad;

  /// No description provided for @retry.
  ///
  /// In en, this message translates to:
  /// **'Retry'**
  String get retry;

  /// No description provided for @newContentIn.
  ///
  /// In en, this message translates to:
  /// **'New content in {time}'**
  String newContentIn(String time);

  /// No description provided for @categoryAnecdote.
  ///
  /// In en, this message translates to:
  /// **'Anecdote'**
  String get categoryAnecdote;

  /// No description provided for @categoryChuckNorris.
  ///
  /// In en, this message translates to:
  /// **'Chuck Norris'**
  String get categoryChuckNorris;

  /// No description provided for @categoryAdvice.
  ///
  /// In en, this message translates to:
  /// **'Celebrity Quote'**
  String get categoryAdvice;

  /// No description provided for @categoryHistory.
  ///
  /// In en, this message translates to:
  /// **'History'**
  String get categoryHistory;

  /// No description provided for @categoryAnimals.
  ///
  /// In en, this message translates to:
  /// **'Animals'**
  String get categoryAnimals;

  /// No description provided for @categoryCountry.
  ///
  /// In en, this message translates to:
  /// **'Countries'**
  String get categoryCountry;

  /// No description provided for @categoryWorld.
  ///
  /// In en, this message translates to:
  /// **'World'**
  String get categoryWorld;

  /// No description provided for @categoryFrenchDepartment.
  ///
  /// In en, this message translates to:
  /// **'French Department'**
  String get categoryFrenchDepartment;

  /// No description provided for @categoryPacificIsland.
  ///
  /// In en, this message translates to:
  /// **'Pacific Island'**
  String get categoryPacificIsland;

  /// No description provided for @categoryExoplanet.
  ///
  /// In en, this message translates to:
  /// **'Exoplanet'**
  String get categoryExoplanet;

  /// No description provided for @showAnecdote.
  ///
  /// In en, this message translates to:
  /// **'Show anecdote'**
  String get showAnecdote;

  /// No description provided for @translate.
  ///
  /// In en, this message translates to:
  /// **'Translate to French'**
  String get translate;

  /// No description provided for @tapToHide.
  ///
  /// In en, this message translates to:
  /// **'Tap again to hide details'**
  String get tapToHide;

  /// No description provided for @error.
  ///
  /// In en, this message translates to:
  /// **'Error'**
  String get error;

  /// No description provided for @translationError.
  ///
  /// In en, this message translates to:
  /// **'Translation error'**
  String get translationError;

  /// No description provided for @english.
  ///
  /// In en, this message translates to:
  /// **'English'**
  String get english;

  /// No description provided for @french.
  ///
  /// In en, this message translates to:
  /// **'French'**
  String get french;

  /// No description provided for @spanish.
  ///
  /// In en, this message translates to:
  /// **'Spanish'**
  String get spanish;

  /// No description provided for @popMillion.
  ///
  /// In en, this message translates to:
  /// **'M'**
  String get popMillion;

  /// No description provided for @popBillion.
  ///
  /// In en, this message translates to:
  /// **'B'**
  String get popBillion;

  /// No description provided for @lightYear.
  ///
  /// In en, this message translates to:
  /// **'ly'**
  String get lightYear;

  /// No description provided for @updateTitle.
  ///
  /// In en, this message translates to:
  /// **'Update available'**
  String get updateTitle;

  /// No description provided for @updateMessage.
  ///
  /// In en, this message translates to:
  /// **'A new version of the app is available. Update to enjoy the latest features.'**
  String get updateMessage;

  /// No description provided for @updateButton.
  ///
  /// In en, this message translates to:
  /// **'Update'**
  String get updateButton;

  /// No description provided for @categorySpace.
  ///
  /// In en, this message translates to:
  /// **'Space'**
  String get categorySpace;

  /// No description provided for @categoryStar.
  ///
  /// In en, this message translates to:
  /// **'Stars'**
  String get categoryStar;

  /// No description provided for @categorySolarSystemMoon.
  ///
  /// In en, this message translates to:
  /// **'Solar System Moons'**
  String get categorySolarSystemMoon;

  /// No description provided for @categoryHistoryHub.
  ///
  /// In en, this message translates to:
  /// **'History'**
  String get categoryHistoryHub;

  /// No description provided for @categoryDayOfHistory.
  ///
  /// In en, this message translates to:
  /// **'Day of History'**
  String get categoryDayOfHistory;

  /// No description provided for @categoryKingOfFrance.
  ///
  /// In en, this message translates to:
  /// **'Kings of France'**
  String get categoryKingOfFrance;

  /// No description provided for @categoryAmericanPresident.
  ///
  /// In en, this message translates to:
  /// **'American Presidents'**
  String get categoryAmericanPresident;

  /// No description provided for @categoryCinemaHub.
  ///
  /// In en, this message translates to:
  /// **'Cinema'**
  String get categoryCinemaHub;

  /// No description provided for @categoryCelebrityHub.
  ///
  /// In en, this message translates to:
  /// **'Celebrity'**
  String get categoryCelebrityHub;

  /// No description provided for @categoryClassicCinema.
  ///
  /// In en, this message translates to:
  /// **'Classic Hollywood'**
  String get categoryClassicCinema;

  /// No description provided for @categoryCinema80s90s.
  ///
  /// In en, this message translates to:
  /// **'80s & 90s Movies'**
  String get categoryCinema80s90s;

  /// No description provided for @categoryModernCinema.
  ///
  /// In en, this message translates to:
  /// **'Modern Cinema'**
  String get categoryModernCinema;

  /// No description provided for @categoryScienceHub.
  ///
  /// In en, this message translates to:
  /// **'Science & Nature'**
  String get categoryScienceHub;

  /// No description provided for @categoryDinosaur.
  ///
  /// In en, this message translates to:
  /// **'Dinosaurs'**
  String get categoryDinosaur;

  /// No description provided for @categorySpaceMission.
  ///
  /// In en, this message translates to:
  /// **'Space Missions'**
  String get categorySpaceMission;

  /// No description provided for @categoryBattle.
  ///
  /// In en, this message translates to:
  /// **'Historical Battles'**
  String get categoryBattle;

  /// No description provided for @categoryArtHub.
  ///
  /// In en, this message translates to:
  /// **'Art & Culture'**
  String get categoryArtHub;

  /// No description provided for @categoryPainting.
  ///
  /// In en, this message translates to:
  /// **'Famous Paintings'**
  String get categoryPainting;

  /// No description provided for @term1.
  ///
  /// In en, this message translates to:
  /// **'1st term'**
  String get term1;

  /// No description provided for @term2.
  ///
  /// In en, this message translates to:
  /// **'2nd term'**
  String get term2;

  /// No description provided for @term3.
  ///
  /// In en, this message translates to:
  /// **'3rd term'**
  String get term3;

  /// No description provided for @term4.
  ///
  /// In en, this message translates to:
  /// **'4th term'**
  String get term4;

  /// No description provided for @voOriginal.
  ///
  /// In en, this message translates to:
  /// **'Original version'**
  String get voOriginal;

  /// No description provided for @voTranslation.
  ///
  /// In en, this message translates to:
  /// **'Translation'**
  String get voTranslation;

  /// No description provided for @dubbing.
  ///
  /// In en, this message translates to:
  /// **'Dubbing'**
  String get dubbing;

  /// No description provided for @hideDubbing.
  ///
  /// In en, this message translates to:
  /// **'Hide dubbing'**
  String get hideDubbing;

  /// No description provided for @categorySculpture.
  ///
  /// In en, this message translates to:
  /// **'Famous Sculptures'**
  String get categorySculpture;

  /// No description provided for @categoryArchitecture.
  ///
  /// In en, this message translates to:
  /// **'Iconic Architecture'**
  String get categoryArchitecture;

  /// No description provided for @categoryFamousArtist.
  ///
  /// In en, this message translates to:
  /// **'Famous Artists'**
  String get categoryFamousArtist;

  /// No description provided for @categoryPhotographer.
  ///
  /// In en, this message translates to:
  /// **'Photographers'**
  String get categoryPhotographer;

  /// No description provided for @categoryClassicalComposer.
  ///
  /// In en, this message translates to:
  /// **'Classical Composers'**
  String get categoryClassicalComposer;

  /// No description provided for @categoryNobelPrize.
  ///
  /// In en, this message translates to:
  /// **'Nobel Prize'**
  String get categoryNobelPrize;

  /// No description provided for @categoryFrenchCommune.
  ///
  /// In en, this message translates to:
  /// **'French Communes'**
  String get categoryFrenchCommune;

  /// No description provided for @categoryAmericanState.
  ///
  /// In en, this message translates to:
  /// **'American States'**
  String get categoryAmericanState;
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(lookupAppLocalizations(locale));
  }

  @override
  bool isSupported(Locale locale) =>
      <String>['en', 'es', 'fr'].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {
  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'en':
      return AppLocalizationsEn();
    case 'es':
      return AppLocalizationsEs();
    case 'fr':
      return AppLocalizationsFr();
  }

  throw FlutterError(
      'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
      'an issue with the localizations generation tool. Please file an issue '
      'on GitHub with a reproducible sample app and the gen-l10n configuration '
      'that was used.');
}

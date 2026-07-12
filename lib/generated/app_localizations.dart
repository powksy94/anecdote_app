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

  /// No description provided for @closeButton.
  ///
  /// In en, this message translates to:
  /// **'Close'**
  String get closeButton;

  /// No description provided for @contentWarningTitle.
  ///
  /// In en, this message translates to:
  /// **'Content Warning'**
  String get contentWarningTitle;

  /// No description provided for @historicalNoteTitle.
  ///
  /// In en, this message translates to:
  /// **'Historical Note'**
  String get historicalNoteTitle;

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
  /// **'New version available!'**
  String get updateTitle;

  /// No description provided for @updateMessage.
  ///
  /// In en, this message translates to:
  /// **'Improvements and new content are waiting for you.'**
  String get updateMessage;

  /// No description provided for @updateButton.
  ///
  /// In en, this message translates to:
  /// **'Update now'**
  String get updateButton;

  /// No description provided for @updateLaterButton.
  ///
  /// In en, this message translates to:
  /// **'Later'**
  String get updateLaterButton;

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

  /// No description provided for @categoryScienceLivingHub.
  ///
  /// In en, this message translates to:
  /// **'Living World'**
  String get categoryScienceLivingHub;

  /// No description provided for @categoryScienceNonLivingHub.
  ///
  /// In en, this message translates to:
  /// **'Non-Living'**
  String get categoryScienceNonLivingHub;

  /// No description provided for @categoryArtWorksHub.
  ///
  /// In en, this message translates to:
  /// **'Art Works'**
  String get categoryArtWorksHub;

  /// No description provided for @categoryArtArtistsHub.
  ///
  /// In en, this message translates to:
  /// **'Artists'**
  String get categoryArtArtistsHub;

  /// No description provided for @categoryChemicalElement.
  ///
  /// In en, this message translates to:
  /// **'Chemical Elements'**
  String get categoryChemicalElement;

  /// No description provided for @categoryVolcano.
  ///
  /// In en, this message translates to:
  /// **'Volcanoes'**
  String get categoryVolcano;

  /// No description provided for @categoryDesert.
  ///
  /// In en, this message translates to:
  /// **'Deserts'**
  String get categoryDesert;

  /// No description provided for @categoryRiver.
  ///
  /// In en, this message translates to:
  /// **'Rivers'**
  String get categoryRiver;

  /// No description provided for @categorySea.
  ///
  /// In en, this message translates to:
  /// **'Seas'**
  String get categorySea;

  /// No description provided for @categoryInsect.
  ///
  /// In en, this message translates to:
  /// **'Insects'**
  String get categoryInsect;

  /// No description provided for @categoryBird.
  ///
  /// In en, this message translates to:
  /// **'Birds'**
  String get categoryBird;

  /// No description provided for @categoryMineral.
  ///
  /// In en, this message translates to:
  /// **'Minerals'**
  String get categoryMineral;

  /// No description provided for @categoryCloud.
  ///
  /// In en, this message translates to:
  /// **'Clouds'**
  String get categoryCloud;

  /// No description provided for @categoryHumanBone.
  ///
  /// In en, this message translates to:
  /// **'Human Bones'**
  String get categoryHumanBone;

  /// No description provided for @categoryTerritoriesHub.
  ///
  /// In en, this message translates to:
  /// **'Territories'**
  String get categoryTerritoriesHub;

  /// No description provided for @categoryNaturalWondersHub.
  ///
  /// In en, this message translates to:
  /// **'Natural Wonders'**
  String get categoryNaturalWondersHub;

  /// No description provided for @noImageTitle.
  ///
  /// In en, this message translates to:
  /// **'Image unavailable'**
  String get noImageTitle;

  /// No description provided for @noImageExplanation.
  ///
  /// In en, this message translates to:
  /// **'This work is still protected by copyright. No free image is currently available.'**
  String get noImageExplanation;

  /// No description provided for @noImageExoplanet.
  ///
  /// In en, this message translates to:
  /// **'🪐 Not directly observable — detected by indirect methods'**
  String get noImageExoplanet;

  /// No description provided for @noImageStar.
  ///
  /// In en, this message translates to:
  /// **'⭐ No telescope image available for this star'**
  String get noImageStar;

  /// No description provided for @noImageSpaceMission.
  ///
  /// In en, this message translates to:
  /// **'🚀 No image available for this mission'**
  String get noImageSpaceMission;

  /// No description provided for @noImageGeneric.
  ///
  /// In en, this message translates to:
  /// **'No image available'**
  String get noImageGeneric;

  /// No description provided for @categoryHumorHub.
  ///
  /// In en, this message translates to:
  /// **'Humor'**
  String get categoryHumorHub;

  /// No description provided for @categoryPersonalityHub.
  ///
  /// In en, this message translates to:
  /// **'Personalities'**
  String get categoryPersonalityHub;

  /// No description provided for @categoryLgbtqiaPersonality.
  ///
  /// In en, this message translates to:
  /// **'LGBTQIA+'**
  String get categoryLgbtqiaPersonality;

  /// No description provided for @categoryPioneerWoman.
  ///
  /// In en, this message translates to:
  /// **'Pioneer Women'**
  String get categoryPioneerWoman;

  /// No description provided for @categoryLegendaryAthlete.
  ///
  /// In en, this message translates to:
  /// **'Legendary Athletes'**
  String get categoryLegendaryAthlete;

  /// No description provided for @noImageLgbtqia.
  ///
  /// In en, this message translates to:
  /// **'No portrait image available for this personality'**
  String get noImageLgbtqia;

  /// No description provided for @noImagePioneerWoman.
  ///
  /// In en, this message translates to:
  /// **'No portrait image available for this pioneer'**
  String get noImagePioneerWoman;

  /// No description provided for @noImageLegendaryAthlete.
  ///
  /// In en, this message translates to:
  /// **'No photo available for this athlete'**
  String get noImageLegendaryAthlete;

  /// No description provided for @orientationUncertain.
  ///
  /// In en, this message translates to:
  /// **'Sexual orientation or gender identity is uncertain or debated by historians'**
  String get orientationUncertain;

  /// No description provided for @insectPhobiaTitle.
  ///
  /// In en, this message translates to:
  /// **'⚠️ Insect Sensitivity'**
  String get insectPhobiaTitle;

  /// No description provided for @insectPhobiaMessage.
  ///
  /// In en, this message translates to:
  /// **'This category contains photos of real insects. If you have entomophobia (insect phobia), we recommend choosing a different category.'**
  String get insectPhobiaMessage;

  /// No description provided for @continueAnyway.
  ///
  /// In en, this message translates to:
  /// **'Continue anyway'**
  String get continueAnyway;

  /// No description provided for @goBack.
  ///
  /// In en, this message translates to:
  /// **'Go back'**
  String get goBack;

  /// No description provided for @categoryGamingHub.
  ///
  /// In en, this message translates to:
  /// **'Gaming'**
  String get categoryGamingHub;

  /// No description provided for @categoryGamesHub.
  ///
  /// In en, this message translates to:
  /// **'Games'**
  String get categoryGamesHub;

  /// No description provided for @categoryGamersHub.
  ///
  /// In en, this message translates to:
  /// **'Gamers'**
  String get categoryGamersHub;

  /// No description provided for @categoryGamingAnecdote.
  ///
  /// In en, this message translates to:
  /// **'Gaming Trivia'**
  String get categoryGamingAnecdote;

  /// No description provided for @categoryGamingNomination.
  ///
  /// In en, this message translates to:
  /// **'Game Awards'**
  String get categoryGamingNomination;

  /// No description provided for @categoryClassicGame.
  ///
  /// In en, this message translates to:
  /// **'Classic Games'**
  String get categoryClassicGame;

  /// No description provided for @categoryWorstGame.
  ///
  /// In en, this message translates to:
  /// **'Worst Games'**
  String get categoryWorstGame;

  /// No description provided for @categoryBannedGame.
  ///
  /// In en, this message translates to:
  /// **'Banned Games'**
  String get categoryBannedGame;

  /// No description provided for @categoryGamingLegend.
  ///
  /// In en, this message translates to:
  /// **'Gaming Legends'**
  String get categoryGamingLegend;

  /// No description provided for @bannedGameWarningTitle.
  ///
  /// In en, this message translates to:
  /// **'⚠️ Sensitive Content'**
  String get bannedGameWarningTitle;

  /// No description provided for @bannedGameWarningMessage.
  ///
  /// In en, this message translates to:
  /// **'This category contains information about games banned for violence, sexual content, or political censorship. Some descriptions may be disturbing. Do you want to continue?'**
  String get bannedGameWarningMessage;

  /// No description provided for @noImageGamingLegend.
  ///
  /// In en, this message translates to:
  /// **'🎮 No image available for this legend'**
  String get noImageGamingLegend;

  /// No description provided for @noImageClassicGame.
  ///
  /// In en, this message translates to:
  /// **'🕹️ No image available — game artwork is under copyright'**
  String get noImageClassicGame;

  /// No description provided for @noImageGamingNomination.
  ///
  /// In en, this message translates to:
  /// **'🏆 No image available — game artwork is under copyright'**
  String get noImageGamingNomination;

  /// No description provided for @noImageWorstGame.
  ///
  /// In en, this message translates to:
  /// **'💀 No image available — game artwork is under copyright'**
  String get noImageWorstGame;

  /// No description provided for @noImageBannedGame.
  ///
  /// In en, this message translates to:
  /// **'🚫 No image available — game artwork is under copyright'**
  String get noImageBannedGame;

  /// No description provided for @navGeneral.
  ///
  /// In en, this message translates to:
  /// **'General'**
  String get navGeneral;

  /// No description provided for @navFavorites.
  ///
  /// In en, this message translates to:
  /// **'Favorites'**
  String get navFavorites;

  /// No description provided for @favoritesTitle.
  ///
  /// In en, this message translates to:
  /// **'My favorites'**
  String get favoritesTitle;

  /// No description provided for @favoritesEmpty.
  ///
  /// In en, this message translates to:
  /// **'No favorites this month'**
  String get favoritesEmpty;

  /// No description provided for @favoritesMonth.
  ///
  /// In en, this message translates to:
  /// **'Your {month} favorites'**
  String favoritesMonth(String month);

  /// No description provided for @loginRequired.
  ///
  /// In en, this message translates to:
  /// **'Sign in required'**
  String get loginRequired;

  /// No description provided for @loginToSaveFavorites.
  ///
  /// In en, this message translates to:
  /// **'Sign in to save your favorite facts.'**
  String get loginToSaveFavorites;

  /// No description provided for @signIn.
  ///
  /// In en, this message translates to:
  /// **'Sign in'**
  String get signIn;

  /// No description provided for @createAccount.
  ///
  /// In en, this message translates to:
  /// **'Create an account'**
  String get createAccount;

  /// No description provided for @emailLabel.
  ///
  /// In en, this message translates to:
  /// **'Email'**
  String get emailLabel;

  /// No description provided for @passwordLabel.
  ///
  /// In en, this message translates to:
  /// **'Password'**
  String get passwordLabel;

  /// No description provided for @confirmPasswordLabel.
  ///
  /// In en, this message translates to:
  /// **'Confirm password'**
  String get confirmPasswordLabel;

  /// No description provided for @firstNameLabel.
  ///
  /// In en, this message translates to:
  /// **'First name'**
  String get firstNameLabel;

  /// No description provided for @requiredField.
  ///
  /// In en, this message translates to:
  /// **'Required'**
  String get requiredField;

  /// No description provided for @nextButton.
  ///
  /// In en, this message translates to:
  /// **'Next'**
  String get nextButton;

  /// No description provided for @skipButton.
  ///
  /// In en, this message translates to:
  /// **'Skip'**
  String get skipButton;

  /// No description provided for @startButton.
  ///
  /// In en, this message translates to:
  /// **'Get started'**
  String get startButton;

  /// No description provided for @signOut.
  ///
  /// In en, this message translates to:
  /// **'Sign out'**
  String get signOut;

  /// No description provided for @noAccountYet.
  ///
  /// In en, this message translates to:
  /// **'Don\'t have an account?'**
  String get noAccountYet;

  /// No description provided for @alreadyHaveAccount.
  ///
  /// In en, this message translates to:
  /// **'Already have an account?'**
  String get alreadyHaveAccount;

  /// No description provided for @invalidEmail.
  ///
  /// In en, this message translates to:
  /// **'Invalid email'**
  String get invalidEmail;

  /// No description provided for @passwordMinLength.
  ///
  /// In en, this message translates to:
  /// **'At least 12 characters'**
  String get passwordMinLength;

  /// No description provided for @passwordsDoNotMatch.
  ///
  /// In en, this message translates to:
  /// **'Passwords do not match'**
  String get passwordsDoNotMatch;

  /// No description provided for @registerTitle.
  ///
  /// In en, this message translates to:
  /// **'Create your account'**
  String get registerTitle;

  /// No description provided for @registerStep1Subtitle.
  ///
  /// In en, this message translates to:
  /// **'Step 1 of 3 — Your credentials'**
  String get registerStep1Subtitle;

  /// No description provided for @registerStep2Title.
  ///
  /// In en, this message translates to:
  /// **'What should we call you?'**
  String get registerStep2Title;

  /// No description provided for @registerStep2Subtitle.
  ///
  /// In en, this message translates to:
  /// **'Step 2 of 3 — Your first name'**
  String get registerStep2Subtitle;

  /// No description provided for @registerStep3Title.
  ///
  /// In en, this message translates to:
  /// **'What are you interested in?'**
  String get registerStep3Title;

  /// No description provided for @registerStep3Subtitle.
  ///
  /// In en, this message translates to:
  /// **'Step 3 of 3 — Choose at least 3 topics'**
  String get registerStep3Subtitle;

  /// No description provided for @chooseAtLeast3.
  ///
  /// In en, this message translates to:
  /// **'Choose at least 3 topics'**
  String get chooseAtLeast3;

  /// No description provided for @themesSelectedCount.
  ///
  /// In en, this message translates to:
  /// **'{count} topic(s) selected'**
  String themesSelectedCount(int count);

  /// No description provided for @authErrorUserNotFound.
  ///
  /// In en, this message translates to:
  /// **'No account found for this email.'**
  String get authErrorUserNotFound;

  /// No description provided for @authErrorWrongPassword.
  ///
  /// In en, this message translates to:
  /// **'Incorrect password.'**
  String get authErrorWrongPassword;

  /// No description provided for @authErrorUserDisabled.
  ///
  /// In en, this message translates to:
  /// **'This account is disabled.'**
  String get authErrorUserDisabled;

  /// No description provided for @authErrorTooManyRequests.
  ///
  /// In en, this message translates to:
  /// **'Too many attempts. Try again later.'**
  String get authErrorTooManyRequests;

  /// No description provided for @authErrorGeneric.
  ///
  /// In en, this message translates to:
  /// **'Connection error. Please try again.'**
  String get authErrorGeneric;

  /// No description provided for @authErrorEmailInUse.
  ///
  /// In en, this message translates to:
  /// **'This email is already in use.'**
  String get authErrorEmailInUse;

  /// No description provided for @authErrorWeakPassword.
  ///
  /// In en, this message translates to:
  /// **'Password is too weak.'**
  String get authErrorWeakPassword;

  /// No description provided for @authErrorAccountCreation.
  ///
  /// In en, this message translates to:
  /// **'Error creating account.'**
  String get authErrorAccountCreation;

  /// No description provided for @onboarding1Title.
  ///
  /// In en, this message translates to:
  /// **'A new discovery every day'**
  String get onboarding1Title;

  /// No description provided for @onboarding1Subtitle.
  ///
  /// In en, this message translates to:
  /// **'Explore dozens of categories: history, science, art, space and much more.'**
  String get onboarding1Subtitle;

  /// No description provided for @onboarding2Title.
  ///
  /// In en, this message translates to:
  /// **'Save your favorites'**
  String get onboarding2Title;

  /// No description provided for @onboarding2Subtitle.
  ///
  /// In en, this message translates to:
  /// **'Keep track of your favorite facts. Find them anytime in the Favorites tab.'**
  String get onboarding2Subtitle;

  /// No description provided for @onboarding2Hint.
  ///
  /// In en, this message translates to:
  /// **'See the Favorites tab at the bottom'**
  String get onboarding2Hint;

  /// No description provided for @onboarding3Title.
  ///
  /// In en, this message translates to:
  /// **'Go Premium'**
  String get onboarding3Title;

  /// No description provided for @onboarding3Subtitle.
  ///
  /// In en, this message translates to:
  /// **'Unlimited favorites, ad-free and access to exclusive content.'**
  String get onboarding3Subtitle;

  /// No description provided for @catAnecdote.
  ///
  /// In en, this message translates to:
  /// **'Anecdotes'**
  String get catAnecdote;

  /// No description provided for @catCinema.
  ///
  /// In en, this message translates to:
  /// **'Cinema'**
  String get catCinema;

  /// No description provided for @catCelebrities.
  ///
  /// In en, this message translates to:
  /// **'Celebrities'**
  String get catCelebrities;

  /// No description provided for @catHistory.
  ///
  /// In en, this message translates to:
  /// **'History'**
  String get catHistory;

  /// No description provided for @catScience.
  ///
  /// In en, this message translates to:
  /// **'Science'**
  String get catScience;

  /// No description provided for @catArt.
  ///
  /// In en, this message translates to:
  /// **'Art'**
  String get catArt;

  /// No description provided for @catWorld.
  ///
  /// In en, this message translates to:
  /// **'World'**
  String get catWorld;

  /// No description provided for @catSpace.
  ///
  /// In en, this message translates to:
  /// **'Space'**
  String get catSpace;

  /// No description provided for @catGaming.
  ///
  /// In en, this message translates to:
  /// **'Gaming'**
  String get catGaming;

  /// No description provided for @catAnimals.
  ///
  /// In en, this message translates to:
  /// **'Animals'**
  String get catAnimals;

  /// No description provided for @catVolcano.
  ///
  /// In en, this message translates to:
  /// **'Volcanoes & Wonders'**
  String get catVolcano;

  /// No description provided for @catDinosaur.
  ///
  /// In en, this message translates to:
  /// **'Dinosaurs'**
  String get catDinosaur;

  /// No description provided for @catArchitecture.
  ///
  /// In en, this message translates to:
  /// **'Architecture'**
  String get catArchitecture;

  /// No description provided for @catMusic.
  ///
  /// In en, this message translates to:
  /// **'Classical music'**
  String get catMusic;

  /// No description provided for @catMineral.
  ///
  /// In en, this message translates to:
  /// **'Minerals'**
  String get catMineral;

  /// No description provided for @catBirds.
  ///
  /// In en, this message translates to:
  /// **'Birds'**
  String get catBirds;

  /// No description provided for @catCloud.
  ///
  /// In en, this message translates to:
  /// **'Clouds'**
  String get catCloud;

  /// No description provided for @catInsects.
  ///
  /// In en, this message translates to:
  /// **'Insects'**
  String get catInsects;
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

import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';
import './core/navigation/root_gate.dart';
import './features/settings/services/notification_preference_service.dart';
import './generated/app_localizations.dart';

final navigatorKey = GlobalKey<NavigatorState>();
final scaffoldMessengerKey = GlobalKey<ScaffoldMessengerState>();

class AnecdoteApp extends StatefulWidget {
  const AnecdoteApp({super.key});

  @override
  State<AnecdoteApp> createState() => _AnecdoteAppState();
}

class _AnecdoteAppState extends State<AnecdoteApp> {
  Locale? _locale;

  @override
  void initState() {
    super.initState();
    _initFCM();
  }

  Future<void> _initFCM() async {
    // Foreground: l'OS Android n'affiche pas les notifs automatiquement
    // quand l'app est ouverte → on affiche un SnackBar
    FirebaseMessaging.onMessage.listen((RemoteMessage message) async {
      final notification = message.notification;
      if (notification == null) return;
      if (!await NotificationPreferenceService().isEnabled()) return;
      scaffoldMessengerKey.currentState?.showSnackBar(
        SnackBar(
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                notification.title ?? '',
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
              if ((notification.body ?? '').isNotEmpty)
                Text(notification.body!),
            ],
          ),
          duration: const Duration(seconds: 6),
          behavior: SnackBarBehavior.floating,
        ),
      );
    });

    // Background tap (app en arrière-plan)
    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
      debugPrint('[FCM] opened from background: ${message.notification?.title}');
    });

    // Token (ciblage par appareil)
    try {
      final token = await FirebaseMessaging.instance.getToken();
      debugPrint('[FCM] token: $token');
    } catch (e) {
      debugPrint('[FCM] getToken error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      navigatorKey: navigatorKey,
      scaffoldMessengerKey: scaffoldMessengerKey,
      locale: _locale,
      supportedLocales: AppLocalizations.supportedLocales,
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      themeMode: ThemeMode.system,
      theme: ThemeData(
        brightness: Brightness.light,
        useMaterial3: true,
        colorSchemeSeed: Colors.indigo,
      ),
      darkTheme: ThemeData(
        brightness: Brightness.dark,
        useMaterial3: true,
        colorSchemeSeed: Colors.indigo,
      ),
      home: RootGate(
        onLocaleChange: (locale) {
          setState(() => _locale = locale);
        },
      ),
    );
  }
}

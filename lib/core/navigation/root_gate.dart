import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../features/auth/pages/welcome_page.dart';
import 'main_shell.dart';

class RootGate extends StatefulWidget {
  final void Function(Locale locale)? onLocaleChange;
  const RootGate({super.key, this.onLocaleChange});

  @override
  State<RootGate> createState() => _RootGateState();
}

class _RootGateState extends State<RootGate> {
  bool? _hasSeenWelcome;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final prefs = await SharedPreferences.getInstance();
    if (mounted) {
      setState(() => _hasSeenWelcome = prefs.getBool('hasSeenWelcome') ?? false);
    }
  }

  Future<void> _proceed() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('hasSeenWelcome', true);
    if (mounted) setState(() => _hasSeenWelcome = true);
  }

  @override
  Widget build(BuildContext context) {
    if (_hasSeenWelcome == null) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    if (!_hasSeenWelcome!) {
      return WelcomePage(onProceed: _proceed);
    }
    return MainShell(onLocaleChange: widget.onLocaleChange);
  }
}

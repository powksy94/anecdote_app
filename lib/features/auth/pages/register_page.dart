import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';
import '../controllers/register_controller.dart';
import '../utils/auth_error_mapper.dart';
import '../widgets/register_step_categories.dart';
import '../widgets/register_step_email.dart';
import '../widgets/register_step_name.dart';
import '../widgets/register_view.dart';
import 'login_page.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  static const int _totalSteps = 3;

  final _controller = RegisterController();
  final _pageCtrl = PageController();
  int _step = 0;

  final _emailCtrl = TextEditingController();
  final _passwordCtrl = TextEditingController();
  final _confirmCtrl = TextEditingController();
  final _step0Key = GlobalKey<FormState>();
  bool _obscure = true;

  final _nameCtrl = TextEditingController();
  final _step1Key = GlobalKey<FormState>();

  final Set<String> _selectedCategories = {};
  bool _loading = false;

  @override
  void dispose() {
    _pageCtrl.dispose();
    _emailCtrl.dispose();
    _passwordCtrl.dispose();
    _confirmCtrl.dispose();
    _nameCtrl.dispose();
    super.dispose();
  }

  void _nextStep() {
    if (_step == 0 && !(_step0Key.currentState?.validate() ?? false)) return;
    if (_step == 1 && !(_step1Key.currentState?.validate() ?? false)) return;
    if (_step < _totalSteps - 1) {
      setState(() => _step++);
      _pageCtrl.animateToPage(_step,
          duration: const Duration(milliseconds: 300), curve: Curves.easeInOut);
    }
  }

  void _prevStep() {
    if (_step > 0) {
      setState(() => _step--);
      _pageCtrl.animateToPage(_step,
          duration: const Duration(milliseconds: 300), curve: Curves.easeInOut);
    } else {
      Navigator.pop(context);
    }
  }

  Future<void> _submit() async {
    final loc = AppLocalizations.of(context)!;
    if (_selectedCategories.length < 3) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(loc.chooseAtLeast3)));
      return;
    }
    setState(() => _loading = true);
    final errorCode = await _controller.createAccount(
      email: _emailCtrl.text.trim(),
      password: _passwordCtrl.text,
      displayName: _nameCtrl.text.trim(),
      categories: _selectedCategories,
    );
    if (!mounted) return;
    setState(() => _loading = false);

    if (errorCode == null) {
      Navigator.of(context).popUntil((r) => r.isFirst);
    } else {
      final msg = AuthErrorMapper.fromRegisterCode(
          AppLocalizations.of(context)!, errorCode);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));
    }
  }

  @override
  Widget build(BuildContext context) {
    return RegisterView(
      step: _step,
      totalSteps: _totalSteps,
      pageCtrl: _pageCtrl,
      onBack: _prevStep,
      stepEmail: RegisterStepEmail(
        formKey: _step0Key,
        emailCtrl: _emailCtrl,
        passwordCtrl: _passwordCtrl,
        confirmCtrl: _confirmCtrl,
        obscure: _obscure,
        onToggleObscure: () => setState(() => _obscure = !_obscure),
        onNext: _nextStep,
        onSignIn: () => Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => const LoginPage()),
        ),
      ),
      stepName: RegisterStepName(
        formKey: _step1Key,
        nameCtrl: _nameCtrl,
        onNext: _nextStep,
      ),
      stepCategories: RegisterStepCategories(
        selected: _selectedCategories,
        onToggle: (id) => setState(() {
          _selectedCategories.contains(id)
              ? _selectedCategories.remove(id)
              : _selectedCategories.add(id);
        }),
        loading: _loading,
        onCreateAccount: _submit,
      ),
    );
  }
}

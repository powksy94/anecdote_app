import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';

class WarningBadge extends StatefulWidget {
  final String text;
  final String level; // "red" or "orange"

  const WarningBadge({required this.text, required this.level, super.key});

  @override
  State<WarningBadge> createState() => _WarningBadgeState();
}

class _WarningBadgeState extends State<WarningBadge>
    with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  late final Animation<double> _fade;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 700),
    )..repeat(reverse: true);
    _fade = Tween<double>(begin: 0.15, end: 1.0).animate(
      CurvedAnimation(parent: _ctrl, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  Color get _color => widget.level == 'red' ? Colors.red : Colors.orange;

  void _showDialog(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    showDialog<void>(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF1E1E2E),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: Row(
          children: [
            Icon(Icons.warning_rounded, color: _color, size: 22),
            const SizedBox(width: 10),
            Text(
              loc.contentWarningTitle,
              style: const TextStyle(color: Colors.white, fontSize: 16),
            ),
          ],
        ),
        content: Text(
          widget.text,
          style: const TextStyle(
            color: Color(0xFFCCCCCC),
            fontSize: 14,
            height: 1.5,
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: Text(loc.closeButton, style: TextStyle(color: _color)),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => _showDialog(context),
      child: FadeTransition(
        opacity: _fade,
        child: Container(
          padding: const EdgeInsets.all(6),
          decoration: BoxDecoration(
            color: Colors.black.withValues(alpha: 0.65),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(Icons.warning_rounded, color: _color, size: 22),
        ),
      ),
    );
  }
}

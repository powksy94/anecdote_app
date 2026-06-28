import 'package:flutter/material.dart';

class InfoNoteBadge extends StatelessWidget {
  final String text;

  const InfoNoteBadge({required this.text, super.key});

  void _showDialog(BuildContext context) {
    showDialog<void>(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF1E1E2E),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: const Row(
          children: [
            Icon(Icons.info_outline_rounded, color: Colors.lightBlueAccent, size: 22),
            SizedBox(width: 10),
            Text('Historical Note', style: TextStyle(color: Colors.white, fontSize: 16)),
          ],
        ),
        content: Text(
          text,
          style: const TextStyle(color: Color(0xFFCCCCCC), fontSize: 14, height: 1.5),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Close', style: TextStyle(color: Colors.lightBlueAccent)),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) => GestureDetector(
        onTap: () => _showDialog(context),
        child: Container(
          padding: const EdgeInsets.all(6),
          decoration: BoxDecoration(
            color: Colors.black.withValues(alpha: 0.65),
            borderRadius: BorderRadius.circular(8),
          ),
          child: const Icon(Icons.info_outline_rounded, color: Colors.lightBlueAccent, size: 22),
        ),
      );
}

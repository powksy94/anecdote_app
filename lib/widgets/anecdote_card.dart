import 'package:flutter/material.dart';

class AnecdoteCard extends StatelessWidget {
  final String text;
  final bool showDetails;
  final VoidCallback onTap;

  const AnecdoteCard({
    super.key,
    required this.text,
    required this.showDetails,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        padding: const EdgeInsets.all(20),
        constraints: BoxConstraints(
          maxHeight: showDetails ? 200 : 100,
          maxWidth: 400,
        ),
        decoration: BoxDecoration(
          color: Colors.indigo[50],
          borderRadius: BorderRadius.circular(20),
          boxShadow: [
            BoxShadow(
              color: Colors.indigo.withOpacity(0.2),
              blurRadius: 10,
            ),
          ],
        ),
        child: Center(
          child: Text(
            text,
            textAlign: TextAlign.center,
            style: const TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ),
    );
  }
}

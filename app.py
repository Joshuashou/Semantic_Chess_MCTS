from flask import Flask, render_template, jsonify, request
import chess
import uvicorn
from engine.evaluator import gpt_analysis
app = Flask(__name__)

game_board = chess.Board()

@app.route('/')
def index():
    # Reset the board when starting a new game
    global game_board
    game_board = chess.Board()
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    # Get the move and position from request
    move = request.json.get('move')
    position = request.json.get('position')
    
    # Convert the move string (e.g., 'e2e4') to chess.Move object
    chess_move = chess.Move.from_uci(move)
    
    # Set up board with current position
    game_board.set_fen(position)
    
    # Apply the move if it's legal
    if chess_move in game_board.legal_moves:
        game_board.push(chess_move)
        
        # Get current position in standard format
        current_position = game_board.fen()
        
        # Pass through LLM step (placeholder for now)
        llm_analysis = gpt_analysis(current_position)
        
        # Get valid moves for next turn
        valid_moves = {}
        for move in game_board.legal_moves:
            from_square = chess.square_name(move.from_square)
            if from_square not in valid_moves:
                valid_moves[from_square] = []
            valid_moves[from_square].append(chess.square_name(move.to_square))
        
        return jsonify({
            'validMoves': valid_moves,
            'fen': current_position,
            'llmAnalysis': llm_analysis
        })
    else:
        return jsonify({'error': 'Invalid move'}), 400

if __name__ == '__main__':
    app.run(debug=True)
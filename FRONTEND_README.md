# 📚 Research Document Summerizer - Frontend

A beautiful and intuitive Streamlit frontend for the Document Analysis & Challenge System that provides a complete workflow for document analysis, question answering, and challenge evaluation.

## 🚀 Features

- **📤 Document Upload**: Upload PDF and TXT files with automatic analysis
- **📋 Auto Summary**: Automatic document summarization after upload
- **❓ Ask Me Anything**: Interactive Q&A mode for document queries
- **🎯 Challenge Mode**: Take AI-generated challenges with detailed evaluation
- **📊 Structured Results**: Beautiful, organized display of evaluation results
- **🎨 Modern UI**: Clean, responsive design with custom styling
- **🔄 Session Management**: Persistent session state with easy reset

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Backend API running on `http://localhost:8000`

### Setup

1. **Install Dependencies**:
   ```bash
   pip install -r frontend_requirements.txt
   ```

2. **Start the Backend** (if not already running):
   ```bash
   # In the backend directory
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

3. **Run the Frontend**:
   ```bash
   streamlit run frontend_app.py
   ```

4. **Access the Application**:
   Open your browser and go to `http://localhost:8501`

## 📖 Usage Guide

### 1. Document Upload
1. Click "Browse files" to select a PDF or TXT document
2. Click "🚀 Upload & Analyze" to process the document
3. The system will automatically generate a summary
4. Session information will appear in the sidebar

### 2. Interaction Modes

#### ❓ Ask Me Anything Mode
- Click "❓ Ask Me Anything" button
- Enter any question about the document
- Click "🔍 Get Answer" to get AI-powered responses
- View both the answer and reference snippets from the document

#### 🎯 Challenge Mode
- Click "🎯 Take Challenge" button
- The system generates 3 logical questions based on the document
- Answer each question in the provided text areas
- Click "🎯 Submit Answers & Get Evaluation" to receive detailed feedback
- View structured results with scores and personalized feedback

### 3. Results Display

#### Challenge Evaluation Results Include:
- **Overall Score**: Percentage-based score with color coding
- **Individual Question Scores**: Detailed scores for each question
- **Personalized Feedback**: Specific feedback for improvement
- **Overall Assessment**: Comprehensive evaluation summary

#### Color Coding:
- 🟢 **Green** (≥70%): Excellent performance
- 🟡 **Yellow** (50-69%): Good performance
- 🔴 **Red** (<50%): Needs improvement

## 🎨 UI Components

### Main Sections
- **Header**: Application title and branding
- **Sidebar**: Navigation, session info, and document summary
- **Main Content**: Dynamic content based on current mode

### Styled Components
- **Success Boxes**: Green background for positive feedback
- **Info Boxes**: Blue background for informational content
- **Question Boxes**: Light gray background for questions
- **Feedback Boxes**: Yellow background for evaluation results

### Responsive Design
- **Wide Layout**: Optimized for desktop and tablet use
- **Column Layouts**: Efficient use of screen space
- **Mobile Friendly**: Responsive design elements

## 🔧 Configuration

### API Configuration
Edit the `API_BASE_URL` in `frontend_app.py`:
```python
API_BASE_URL = "http://localhost:8000"  # Change to your backend URL
```

### Custom Styling
Modify the CSS in the `main()` function to customize:
- Colors and themes
- Font sizes and styles
- Layout spacing
- Component styling

## 📁 File Structure

```
├── frontend_app.py              # Main Streamlit application
├── frontend_requirements.txt    # Frontend dependencies
├── FRONTEND_README.md          # This documentation
└── .streamlit/                 # Streamlit configuration (optional)
    └── config.toml
```

## 🚀 Advanced Features

### Session Management
- **Persistent State**: Session data persists across page refreshes
- **Easy Reset**: One-click session reset for new documents
- **State Validation**: Automatic validation of session data

### Error Handling
- **API Errors**: Graceful handling of backend communication errors
- **Validation**: Input validation for all user interactions
- **User Feedback**: Clear error messages and success notifications

### Performance Optimizations
- **Lazy Loading**: Questions generated only when needed
- **Caching**: Session state caching for better performance
- **Async Operations**: Non-blocking UI during API calls

## 🔍 Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Ensure the backend is running on `http://localhost:8000`
   - Check if the API endpoints are accessible
   - Verify network connectivity

2. **File Upload Issues**
   - Ensure file is PDF or TXT format
   - Check file size (max 10MB recommended)
   - Verify file is not corrupted

3. **Session State Issues**
   - Use the "🔄 Upload New Document" button to reset
   - Refresh the page if needed
   - Clear browser cache if problems persist

### Debug Mode
Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🎯 Workflow Examples

### Complete Challenge Workflow
1. Upload document → Get summary
2. Click "🎯 Take Challenge"
3. Answer 3 generated questions
4. Submit and receive detailed evaluation
5. Review scores and feedback
6. Optionally retry or upload new document

### Q&A Workflow
1. Upload document → Get summary
2. Click "❓ Ask Me Anything"
3. Ask multiple questions about the document
4. Get AI-powered answers with references
5. Continue asking or switch to challenge mode

## 🔮 Future Enhancements

- **Export Results**: PDF/CSV export of evaluation results
- **Question History**: Save and review previous questions
- **Custom Themes**: User-selectable UI themes
- **Offline Mode**: Basic functionality without backend
- **Multi-language Support**: Internationalization
- **Advanced Analytics**: Detailed performance metrics
- **Collaborative Features**: Share results and challenges

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify backend API is running
3. Review error messages in the application
4. Check browser console for additional details

## 📄 License

This frontend is part of the Document Analysis & Challenge System. 
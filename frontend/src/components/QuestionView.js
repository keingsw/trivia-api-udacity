import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      view: 'list',
      searchTerm: null,
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: [],
      currentCategory: null,
    };
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.page}`,
      type: 'GET',
      success: result => {
        this.setState({
          view: 'list',
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category,
        });
        return;
      },
      error: error => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  selectPage(num) {
    if (this.state.view === 'search') {
      this.setState({ page: num }, () => this.search());
    } else {
      this.setState({ page: num }, () => this.getQuestions());
    }
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = () => {
    const { page, currentCategory } = this.state;

    $.ajax({
      url: `/categories/${currentCategory}/questions?page=${page}`,
      type: 'GET',
      success: result => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: error => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  handleCategoryClick = categoryId => {
    this.setState(
      {
        view: 'in_category',
        page: 1,
        currentCategory: categoryId,
      },
      () => this.getByCategory()
    );
  };

  search = () => {
    const { page, searchTerm } = this.state;

    $.ajax({
      url: `/questions?page=${page}`,
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ search_term: searchTerm }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: result => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: error => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };
  submitSearch = searchTerm => {
    this.setState(
      {
        view: 'search',
        page: 1,
        searchTerm: searchTerm,
      },
      () => this.search()
    );
  };

  questionAction = id => action => {
    if (action === 'DELETE') {
      if (window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`,
          type: 'DELETE',
          success: result => {
            this.getQuestions();
          },
          error: error => {
            alert('Unable to load questions. Please try your request again');
            return;
          },
        });
      }
    }
  };

  render() {
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2
            onClick={() => {
              this.getQuestions();
            }}
          >
            Categories
          </h2>
          <ul>
            {this.state.categories.map(category =>
              <li
                key={category.id}
                onClick={() => {
                  this.handleCategoryClick(category.id);
                }}
              >
                {category.type}
                <img
                  className="category"
                  src={`${category.type}.svg`}
                  alt={`Category ${category.type}`}
                />
              </li>
            )}
          </ul>
          <Search submitSearch={this.submitSearch} />
        </div>
        <div className="questions-list">
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) =>
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={
                this.state.categories.filter(c => c.id === q.category)[0].type
              }
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          )}
          <div className="pagination-menu">
            {this.createPagination()}
          </div>
        </div>
      </div>
    );
  }
}

export default QuestionView;

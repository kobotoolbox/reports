
'use strict';

import React from 'react';
import reactMixin from 'react-mixin';
import Reflux from 'reflux';
import bem from '../libs/react-create-bem-element';
import bemRouterLink from '../libs/bemRouterLink';
import moment from 'moment';
import {RequireLoggedIn} from '../mixins/requireLogins';
import actions from '../actions/actions';
import {renderingsStore} from '../stores/renderings';
import Modal from 'react-modal';

require('styles/ProjectList.scss');

var Content = bem('content'),
    ContentBg = bem('content-bg'),
    ContentTitle = bem('content-title', '<h2>'),
    Navlink = bemRouterLink('navlink'),
    BorderedNavlink = bemRouterLink('bordered-navlink'),
    ProjectUl = bem('project-list', '<ul>'),
    ProjectLi = bem('project-list__item', '<li>'),
    ProjectAttribute = bem('project__attribute', '<span>'),
    ProjectAttributeGroup = bem('project__attribute-group', '<div>'),
    ProjectAttributeLink = bem('project__attribute-link', '<a>');

class ProjectList extends Reflux.Component {
  constructor (props) {
    super(props);
    this.state = {
      projects: [],
      projectsLoading: true,
      syncingProject: false,
      copiedLink: '',
      modalIsOpen: false,
      formBuilder: {url: null}
    };
  }
  componentDidMount () {
    this.listenTo(renderingsStore, this.renderingsStoreChanged);
    actions.listRenderings();
  }
  copyText (evt) {
    var $ect = evt.currentTarget;
    navigator.clipboard.writeText($ect.dataset.textToCopy).then(
      this.afterCopy.bind(this)
    );
  }
  syncProject (evt) {
    var $ect = evt.currentTarget;
    this.setState({
      syncingProject: parseInt($ect.dataset.projectId),
    });
    actions.syncProject($ect.dataset.projectId);
  }
  renderingsStoreChanged (state) {
    this.setState(state);
  }
  afterCopy () {
    this.state.copiedLink = 'visible';
    this.setState(this.state);
    setTimeout(function() {
      this.state.copiedLink = '';
      this.setState(this.state);
    }.bind(this), 2000);
  }
  openUpdateModal (evt) {
    var $ect = evt.currentTarget;
    this.setState({
      formBuilder: {url: $ect.dataset.editLink}
    });
    this.setState({modalType: 'update', modalIsOpen: true});
  }
  openDeleteModal (evt) {
    var $ect = evt.currentTarget;
    this.setState({
      modalType: 'delete',
      projectId: $ect.dataset.projectId,
      deletePending: false,
      modalIsOpen: true
    });
  }
  closeModal () {
    setTimeout(() => {
      this.setState({modalIsOpen: false});
    }, 0);
  }
  deleteProject () {
    this.setState({deletePending: true});
    actions.deleteRendering(this.state.projectId);
  }
  render () {
    // var projects = [
    //   {name: 'a1', created: new Date(), submission_count: 2, enter_data_link: '1234', id: 1},
    //   {name: 'a2', created: new Date(), submission_count: 3, enter_data_link: '1234', id: 2},
    //   {name: 'a3', created: new Date(), submission_count: 4, enter_data_link: '1234', id: 3},
    //   {name: 'a4', created: new Date(), submission_count: 0, enter_data_link: '1234', id: 4},
    // ];

    return (
        <Content m='project-list'>
          <RequireLoggedIn failTo='/getting-started' />
          <ContentBg>
            <ContentTitle>My Surveys</ContentTitle>
            <p>This page contains a list of your survey projects. Each survey is assigned a unique URL that can be used by multiple data collectors at the same time. Simply copy the link and send it to your data collectors. Remember, surveys can be conducted online or offline. Before viewing a report, be sure to click "sync" to update all data collected and to see the most up-to-date results. </p>
            <p>Each survey shows the number of submissions, or surveys with complete data uploaded to the project. Click on the "sync" button to update data collected across all survey enumerators. Under "View report" select how you would like to view your survey results: in your browser, as a PDF or as a Word document.</p>
            <p>For more information about how to use the tool, click <a href="https://www.equitytool.org/data-collection-options/">here</a>.</p>
            <div className="new-project-wrapper" >
              <BorderedNavlink m='new-project' to='/new-project'>
                New survey
              </BorderedNavlink>
            </div>
            <ProjectUl>
              {this.state.projects.length === 0 ?
                <ProjectLi m={this.state.projectsLoading ? 'loadingmessage' : 'notification'}>
                  <i />
                  {this.state.projectsLoading ?
                    'Loading survey list'
                  :
                    'You have no surveys to display. Click "new survey" below.'
                  }
                </ProjectLi>
              : null}

              <div className={this.state.copiedLink + ' link-copied'}>
                Link copied to clipboard
              </div>

              {this.state.projects.map(({name, submission_count, enter_data_link, created, form__name, /*template__name,*/ id, edit_link}) => {
                var dateStr = moment(new Date(created)).format('D MMMM YYYY');
                var hasSubmissions = submission_count > 0;
                var isSyncing = this.state.syncingProject !== false && this.state.syncingProject === id;
                return (
                    <ProjectLi key={`project-${name}`}>
                      <ProjectAttribute m='name'>
                        {name}
                      </ProjectAttribute>
                      <ProjectAttributeGroup>
                        <ProjectAttribute m='date-created'>
                          Created on {dateStr}
                        </ProjectAttribute>
                        <ProjectAttribute m='form-and-template-name'>
                          Collected using {form__name} {/*({template__name})*/}
                        </ProjectAttribute>
                      </ProjectAttributeGroup>
                      <ProjectAttribute m='content'>
                        <ProjectAttribute m='data-collections'>
                          <label>Data collection link: </label>
                          <ProjectAttributeLink m='enter-data' href={enter_data_link} target='_blank'>
                            enter data
                          </ProjectAttributeLink>
                          <button
                            className="button-copy"
                            onClick={this.copyText.bind(this)}
                            data-text-to-copy={enter_data_link}
                          >
                            copy link
                          </button>
                        </ProjectAttribute>
                        <ProjectAttribute m='submissions'>
                          <label>{submission_count} submissions</label>
                          <ProjectAttribute m={{
                            sync: true,
                            syncpending: isSyncing,
                          }} onClick={this.syncProject.bind(this)} data-project-id={id}>
                            <i />
                            sync
                          </ProjectAttribute>
                        </ProjectAttribute>
                        {hasSubmissions ?
                          <ProjectAttribute m='view-report'>
                            <label>View report:</label>
                              <Navlink m='view-report' to={`/report/${id}`}> 
                                view report
                              </Navlink>
                          </ProjectAttribute>
                        : (
                          edit_link ?
                            <ProjectAttribute m='update-form'>
                              <label>Update form: </label>
                              <ProjectAttribute onClick={this.openUpdateModal.bind(this)} data-edit-link={edit_link}>
                                <i />
                                add questions
                              </ProjectAttribute>
                            </ProjectAttribute>
                          :
                            null
                        )}
                        <ProjectAttribute m='danger-zone'>
                          <ProjectAttribute onClick={this.openDeleteModal.bind(this)} data-project-id={id}>
                            <i />
                          </ProjectAttribute>
                        </ProjectAttribute>
                      </ProjectAttribute>
                    </ProjectLi>
                  );
              })}
            </ProjectUl>
          </ContentBg>
          <Modal
            isOpen={this.state.modalIsOpen}
            onRequestClose={this.closeModal.bind(this)}
          >
            {this.state.modalType === 'update' ?
              <div>
                <p>WARNING! Do not edit, delete, or modify the text, format,
                numbers, response options, or calculations generated
                automatically in this form. These fields are required for the
                EquityTool and should not be changed in any way. You may add
                additional questions by clicking the “+” but no changes should
                be made to the existing content. Visit <a target="_blank"
                href="https://equitytool.org/addingquestions">
                equitytool.org/addingquestions</a> for information on how to
                safely add questions to this form.</p>
                <p>After you have added your questions, click preview to test
                your form. To make the changes live in your form, click Save,
                then the 'x' button, and then click Redeploy.</p>
                <div className="modal-buttons">
                  <a
                    href={this.state.formBuilder.url}
                    target="_blank"
                    onClick={this.closeModal.bind(this)}
                  >
                    OK, I understand
                  </a>
                  <button type="button" onClick={this.closeModal.bind(this)}>Cancel</button>
                </div>
              </div>
            : this.state.modalType === 'delete' ?
              <div>
                <p> Are you sure you want to remove this survey from your
                survey list? Please understand that this will permanently
                delete your project data as well as your EquityTool report.
                </p>
                { this.state.deletePending ?
                  <div className="modal-buttons">
                      <button disabled>Deleting your survey...</button>
                  </div>
                :
                  <div className="modal-buttons">
                      <button onClick={this.closeModal.bind(this)}>Cancel</button>
                      <button onClick={this.deleteProject.bind(this)}>
                        OK
                      </button>
                  </div>
                }
              </div>
            :
              <i /> // unknown modal type
          }
          </Modal>

        </Content>
      );
  }
}

reactMixin(ProjectList.prototype, Reflux.ListenerMixin);

export default ProjectList;

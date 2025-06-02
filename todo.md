# Todo Template for SQL Database Projects

## Symbol Guide

| Symbol | Meaning                   | Example Use Case              |
|--------|---------------------------|-------------------------------|
| `[ ]`  | Unstarted task            | `- [ ] Create schema draft`   |
| `[x]`  | Completed task            | `- [x] Implement indexes`     |
| `[-]`  | In-progress               | `- [-] Query optimization`    |
| `[~]`  | On hold                   | `- [~] Partitioning strategy` |
| `[>]`  | Delegated/postponed       | `- [>] Legacy data migration` |
| `[!]`  | High priority             | `- [!] Security audit`        |
| `[?]`  | Needs research            | `- [?] NoSQL hybrid approach` |
| `[@]`  | Requires discussion       | `- [@] Normalization level`   |
| `[$]`  | Budget-related            | `- [$] Cloud DB instance`     |
| `[#]`  | Medium priority           | `- [#] Backup schedule`       |
| `[%]`  | Percentage completed      | `- [% 60] Data validation`    |
| `[→]`  | Moved to another section | `- [→] Moved to documentation`|
| `[⚠]`  | Critical issue            | `- [⚠] Deadlock resolution`   |

The markdown maintains compatibility with GitHub/GitLab rendering while adding enhanced task management features:

- Schema version control tracking
- Query optimization workflows
- ACID compliance checks
- Cloud database considerations
- Performance tuning tasks
- Data lifecycle management
- DBMS-specific feature implementation

**Editing Instructions:**  

- Add DBMS-specific features  
- Include compliance requirements (GDPR/HIPAA)  
- Attach query examples  
- Update connection pool settings  
- Add monitoring tasks

## Customization Guide
```markdown
1. **Priority Mapping**  
   `(!) → High | (#) → Medium | ( ) → Low`

2. **Status Indicators**  
   Combine symbols: `- [x][!] Completed security patch`

3. **Progress Tracking**  
   Use percentages: `- [% 85] ETL pipeline`

4. **Team Coordination**  
   `(@) = DBA review needed | (&) = Cross-team task`

5. **Custom Symbols**  
   Add project-specific markers:

| Custom Symbol | Meaning              |
|---------------|----------------------|
| `[🔍]`         | Query optimization  |
| `[🗄]`         | Schema design       |
| `[🔄]`         | Replication setup   |
| `[📊]`         | Reporting needs     |
| `[🔗]`         | API integrations    |
```

## Project Setup
```markdown
- [ ] [!] Choose DBMS (PostgreSQL/MySQL)
- [ ] [@] Create database architecture document
- [ ] [ ] Initialize core components:
- [ ] Schema.sql (table definitions)
- [ ] Seeds.sql (initial data)
- [ ] Migrations/ (version control)
- [ ] Queries/ (common SQL files)
- [ ] [#] Set up user roles/permissions
- [ ] [~] Cloud vs on-prem decision
- [ ] [$] License cost evaluation
- [ ] [>] Backup system configuration
```

## Development Milestones

### Schema Design
```markdown
- [ ] [⚠] Primary key strategy
- [ ] [@] Normalization level discussion
- [ ] [ ] Indexing plan
- [ ] [#] Data types validation
- [ ] [~] JSONB column requirements
```

### Data Management
```markdown
- [ ] [!] CRUD operations design
- [ ] [ ] Stored procedures
- [ ] [🔍] Query optimization
- [ ] [$] Data encryption setup
- [ ] [% 40] ETL pipeline
```

### Security & Maintenance
```markdown
- [ ] [!] User access controls
- [ ] [@] Backup/recovery strategy
- [ ] [ ] Audit logging
- [ ] [⚠] Vulnerability patches
- [ ] [?] Replication setup
```

### Performance & Testing
```markdown
- [ ] [🗄] Explain analyze reports
- [ ] [ ] Load testing
- [ ] [#] Query plan caching
- [ ] [~] Benchmark comparisons
- [ ] [% 25] Unit tests
```

---

*Last Updated: 2023-12-01*  
*Template Version: 2.1*  
*Supported DBMS: PostgreSQL 15+, MySQL 8+*



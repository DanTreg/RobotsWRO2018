using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web;
using Newtonsoft.Json;

//Базовые методы по записи и чтению из БД

namespace ASP.NET_MVC_Application.Repositories
{
    public class Entity
    {
        public int Id { get; set; }
        public bool IsDeleted { get; set; }
    }

    public abstract class BaseRepository<T> where T : Entity
    {
        private object _sync = new object();

        public virtual T Create(T entity)
        {
            var all = GetAll(true);
            var last = all.OrderByDescending(x => x.Id).FirstOrDefault();

            entity.Id = (last?.Id + 1) ?? 1;
            all.Add(entity);

            WriteAll(all);
            return entity;
        }

        public T Update(T entity)
        {
            var all = GetAll();
            var ent = all.FirstOrDefault(x => x.Id == entity.Id);
            if (ent == null)
            {
                return Create(entity);
            }

            all.Remove(ent);
            all.Add(entity);
            WriteAll(all);
            return entity;
        }

        public T GetById(int id)
        {
            var all = GetAll();
            var ent = all.FirstOrDefault(x => x.Id == id);
            return ent;
        }

        public void Delete(T entity)
        {
            entity.IsDeleted = true;
            Update(entity);
        }



        public virtual List<T> GetAll(bool includeDeleted = false)
        {
            lock (_sync)
            {
                try
                {
                    var file = GetFile();
                    var raw = File.ReadAllText(file);
                    var obj = JsonConvert.DeserializeObject<List<T>>(raw);

                    if (includeDeleted)
                    {
                        return obj.OrderByDescending(x=>x.Id).ToList();
                    }

                    return obj.Where(x => !x.IsDeleted).OrderByDescending(x=>x.Id).ToList();
                }
                catch (Exception e)
                {
                    return new List<T>();
                }
            }
        }


        private void WriteAll(List<T> items)
        {
            lock (_sync)
            {
                var file = GetFile();
                var text = JsonConvert.SerializeObject(items);
                File.WriteAllText(file, text);
            }
        }

        private string GetFile()
        {
            var productFile = HttpContext.Current.Server.MapPath($"~/App_Data/{EntityName}.json");
            if (!File.Exists(productFile))
            {
                File.Create(productFile);
                // initial array
                File.WriteAllText(productFile, "[]");
            }

            return productFile;
        }

        protected abstract string EntityName { get; }
    }
}